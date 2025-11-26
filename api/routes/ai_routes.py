"""
AI Assistance Routes
API endpoints for AI-powered content generation and suggestions
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import httpx

from ..database import db, row_to_dict
from ..auth.decorators import require_auth
from ..config import get_config

config = get_config()

ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')


class AIService:
    """Interface with AI service (Parallel AI or similar)"""

    def __init__(self):
        self.api_key = config.PARALLEL_AI_API_KEY
        self.api_url = config.PARALLEL_AI_API_URL or "https://api.parallelai.com/v1"

    async def generate_text(self, prompt: str, max_tokens: int = 500) -> str:
        """Generate text using AI"""
        if not self.api_key:
            raise Exception("AI service not configured")

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "prompt": prompt,
                    "max_tokens": max_tokens,
                    "temperature": 0.7
                },
                timeout=30.0
            )

            if response.status_code != 200:
                raise Exception(f"AI service error: {response.text}")

            data = response.json()
            return data.get('text', '')

    async def improve_text(self, text: str, instruction: str = "improve") -> str:
        """Improve existing text"""
        prompt = f"Improve the following text ({instruction}):\n\n{text}\n\nImproved version:"
        return await self.generate_text(prompt)

    async def generate_summary(self, text: str, max_length: int = 200) -> str:
        """Generate summary of text"""
        prompt = f"Summarize the following in {max_length} characters or less:\n\n{text}\n\nSummary:"
        return await self.generate_text(prompt, max_tokens=100)


ai_service = AIService()


@ai_bp.route('/suggest-bio', methods=['POST'])
@require_auth
async def suggest_bio():
    """Generate bio suggestions based on profile data"""
    try:
        data = request.get_json()
        context = data.get('context', {})

        # Build prompt from context
        prompt_parts = ["Generate a professional bio for a lateral entry officer"]

        if context.get('position'):
            prompt_parts.append(f"Position: {context['position']}")

        if context.get('department'):
            prompt_parts.append(f"Department: {context['department']}")

        if context.get('expertise'):
            prompt_parts.append(f"Areas of expertise: {context['expertise']}")

        prompt = f"{'. '.join(prompt_parts)}.\n\nProfessional bio:"

        # Generate
        bio = await ai_service.generate_text(prompt, max_tokens=300)

        # Save suggestion
        suggestion_id = db.insert("""
            INSERT INTO ai_suggestions (
                user_id, suggestion_type, input_data, output_data, status
            )
            VALUES (?, 'bio_generation', ?, ?, 'generated')
        """, (
            request.current_user['user_id'],
            str(context),
            bio
        ))

        # Track usage
        db.insert("""
            INSERT INTO ai_usage (
                user_id, feature_type, tokens_used
            )
            VALUES (?, 'bio_generation', 300)
        """, (request.current_user['user_id'],))

        return jsonify({
            'success': True,
            'suggestion': bio,
            'suggestion_id': suggestion_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@ai_bp.route('/improve-text', methods=['POST'])
@require_auth
async def improve_text():
    """Improve/enhance user-provided text"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        field_type = data.get('field_type', 'general')

        if not text:
            return jsonify({'error': 'Text is required'}), 400

        # Generate improvement instructions based on field type
        instructions = {
            'bio': 'make it more professional and concise',
            'achievements': 'make it more impactful and quantifiable',
            'responsibilities': 'make it clearer and more structured',
            'general': 'improve clarity and professionalism'
        }

        instruction = instructions.get(field_type, instructions['general'])

        # Improve text
        improved = await ai_service.improve_text(text, instruction)

        # Save suggestion
        suggestion_id = db.insert("""
            INSERT INTO ai_suggestions (
                user_id, suggestion_type, input_data, output_data, status
            )
            VALUES (?, 'text_improvement', ?, ?, 'generated')
        """, (
            request.current_user['user_id'],
            text,
            improved
        ))

        # Track usage
        db.insert("""
            INSERT INTO ai_usage (
                user_id, feature_type, tokens_used
            )
            VALUES (?, 'text_improvement', 500)
        """, (request.current_user['user_id'],))

        return jsonify({
            'success': True,
            'original': text,
            'improved': improved,
            'suggestion_id': suggestion_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@ai_bp.route('/accept-suggestion/<int:suggestion_id>', methods='POST'])
@require_auth
def accept_suggestion(suggestion_id):
    """Mark AI suggestion as accepted/used"""
    try:
        # Verify ownership
        suggestion = db.execute_one("""
            SELECT * FROM ai_suggestions WHERE id = ? AND user_id = ?
        """, (suggestion_id, request.current_user['user_id']))

        if not suggestion:
            return jsonify({'error': 'Suggestion not found'}), 404

        # Mark as accepted
        db.execute("""
            UPDATE ai_suggestions
            SET status = 'accepted', accepted_at = ?
            WHERE id = ?
        """, (datetime.now(), suggestion_id))

        return jsonify({
            'success': True,
            'message': 'Suggestion accepted'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@ai_bp.route('/usage-stats', methods=['GET'])
@require_auth
def get_usage_stats():
    """Get AI usage statistics for current user"""
    try:
        stats = db.execute("""
            SELECT
                feature_type,
                COUNT(*) as count,
                SUM(tokens_used) as total_tokens
            FROM ai_usage
            WHERE user_id = ?
            GROUP BY feature_type
        """, (request.current_user['user_id'],))

        return jsonify({
            'success': True,
            'stats': [row_to_dict(s) for s in stats]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
