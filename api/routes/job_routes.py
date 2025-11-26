"""
Job Monitoring Routes
API endpoints for AI-powered job discovery and matching
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import httpx

from ..database import db, row_to_dict
from ..auth.decorators import require_auth, optional_auth
from ..config import get_config

config = get_config()

job_bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')


class JobMonitoringService:
    """AI-powered job discovery using Parallel AI"""

    def __init__(self):
        self.api_key = config.PARALLEL_AI_API_KEY
        self.api_url = config.PARALLEL_AI_API_URL or "https://api.parallelai.com/v1"

    async def discover_jobs(self, search_query: str, location: str = None, max_results: int = 50) -> list:
        """Discover jobs using AI web search"""
        if not self.api_key:
            return []

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/search",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "query": search_query,
                    "location": location,
                    "max_results": max_results,
                    "filters": {
                        "job_boards": True,
                        "company_websites": True
                    }
                },
                timeout=60.0
            )

            if response.status_code != 200:
                return []

            data = response.json()
            return data.get('results', [])

    async def calculate_relevance(self, job: dict, user_preferences: dict) -> float:
        """Calculate job relevance score using AI"""
        # Simple relevance scoring (can be enhanced with AI)
        score = 0.0

        # Match keywords
        if user_preferences.get('keywords'):
            keywords = user_preferences['keywords'].lower().split(',')
            job_text = f"{job.get('title', '')} {job.get('description', '')}".lower()

            matched = sum(1 for kw in keywords if kw.strip() in job_text)
            score += (matched / len(keywords)) * 0.4

        # Match location
        if user_preferences.get('preferred_locations') and job.get('location'):
            if any(loc.strip().lower() in job['location'].lower()
                   for loc in user_preferences['preferred_locations'].split(',')):
                score += 0.3

        # Match experience level
        if user_preferences.get('experience_level'):
            if user_preferences['experience_level'].lower() in job.get('experience_level', '').lower():
                score += 0.3

        return min(score, 1.0)


job_monitoring_service = JobMonitoringService()


@job_bp.route('', methods=['GET'])
@optional_auth
def get_jobs():
    """Get all job listings"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        domain = request.args.get('domain', '')
        search = request.args.get('search', '')

        offset = (page - 1) * per_page
        viewer_user = getattr(request, 'current_user', None)

        # Build query
        where_clauses = ["status = 'active'"]
        params = []

        if domain:
            where_clauses.append("domain = ?")
            params.append(domain)

        if search:
            where_clauses.append("(title LIKE ? OR description LIKE ?)")
            params.extend([f'%{search}%', f'%{search}%'])

        where_clause = " AND ".join(where_clauses)

        # Get total count
        count_query = f"SELECT COUNT(*) as count FROM job_listings WHERE {where_clause}"
        count_result = db.execute_one(count_query, params)
        total = count_result['count'] if count_result else 0

        # Get jobs
        query = f"""
            SELECT * FROM job_listings
            WHERE {where_clause}
            ORDER BY posted_date DESC
            LIMIT ? OFFSET ?
        """
        params.extend([per_page, offset])
        jobs = db.execute(query, params)

        return jsonify({
            'success': True,
            'jobs': [row_to_dict(j) for j in jobs],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@job_bp.route('/domains', methods=['GET'])
def get_job_domains():
    """Get all job domains"""
    try:
        domains = db.execute("""
            SELECT * FROM job_domains ORDER BY name
        """)

        return jsonify({
            'success': True,
            'domains': [row_to_dict(d) for d in domains]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@job_bp.route('/preferences', methods=['GET'])
@require_auth
def get_job_preferences():
    """Get user's job preferences"""
    try:
        prefs = db.execute_one("""
            SELECT * FROM user_job_preferences
            WHERE user_id = ?
        """, (request.current_user['user_id'],))

        if prefs:
            return jsonify({
                'success': True,
                'preferences': row_to_dict(prefs)
            })
        else:
            return jsonify({
                'success': True,
                'preferences': None
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@job_bp.route('/preferences', methods=['POST'])
@require_auth
def update_job_preferences():
    """Update job preferences"""
    try:
        data = request.get_json()

        # Check if preferences exist
        existing = db.execute_one("""
            SELECT id FROM user_job_preferences WHERE user_id = ?
        """, (request.current_user['user_id'],))

        if existing:
            # Update
            db.execute("""
                UPDATE user_job_preferences
                SET keywords = ?, preferred_locations = ?, experience_level = ?,
                    job_types = ?, salary_range_min = ?, salary_range_max = ?,
                    notifications_enabled = ?
                WHERE user_id = ?
            """, (
                data.get('keywords'),
                data.get('preferred_locations'),
                data.get('experience_level'),
                data.get('job_types'),
                data.get('salary_range_min'),
                data.get('salary_range_max'),
                data.get('notifications_enabled', True),
                request.current_user['user_id']
            ))
        else:
            # Insert
            db.insert("""
                INSERT INTO user_job_preferences (
                    user_id, keywords, preferred_locations, experience_level,
                    job_types, salary_range_min, salary_range_max, notifications_enabled
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                request.current_user['user_id'],
                data.get('keywords'),
                data.get('preferred_locations'),
                data.get('experience_level'),
                data.get('job_types'),
                data.get('salary_range_min'),
                data.get('salary_range_max'),
                data.get('notifications_enabled', True)
            ))

        return jsonify({
            'success': True,
            'message': 'Job preferences updated'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@job_bp.route('/saved', methods=['GET'])
@require_auth
def get_saved_jobs():
    """Get user's saved jobs"""
    try:
        saved = db.execute("""
            SELECT sj.*, jl.*
            FROM saved_jobs sj
            JOIN job_listings jl ON sj.job_id = jl.id
            WHERE sj.user_id = ?
            ORDER BY sj.saved_at DESC
        """, (request.current_user['user_id'],))

        return jsonify({
            'success': True,
            'jobs': [row_to_dict(j) for j in saved]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@job_bp.route('/<int:job_id>/save', methods=['POST'])
@require_auth
def save_job(job_id):
    """Save a job"""
    try:
        # Check if already saved
        existing = db.execute_one("""
            SELECT id FROM saved_jobs WHERE user_id = ? AND job_id = ?
        """, (request.current_user['user_id'], job_id))

        if existing:
            return jsonify({'error': 'Job already saved'}), 400

        # Save
        db.insert("""
            INSERT INTO saved_jobs (user_id, job_id)
            VALUES (?, ?)
        """, (request.current_user['user_id'], job_id))

        return jsonify({
            'success': True,
            'message': 'Job saved'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@job_bp.route('/<int:job_id>/unsave', methods=['POST'])
@require_auth
def unsave_job(job_id):
    """Remove saved job"""
    try:
        db.execute("""
            DELETE FROM saved_jobs WHERE user_id = ? AND job_id = ?
        """, (request.current_user['user_id'], job_id))

        return jsonify({
            'success': True,
            'message': 'Job removed from saved'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@job_bp.route('/discover', methods=['POST'])
@require_auth
async def discover_new_jobs():
    """Trigger AI job discovery (admin or scheduled task)"""
    try:
        # Check if user is admin
        if request.current_user['role'] != 'admin':
            return jsonify({'error': 'Admin only'}), 403

        data = request.get_json()
        domain = data.get('domain', 'general')
        search_query = data.get('query', 'government jobs India')

        # Discover jobs
        jobs = await job_monitoring_service.discover_jobs(search_query)

        # Store in database
        inserted = 0
        for job_data in jobs:
            try:
                db.insert("""
                    INSERT INTO job_listings (
                        title, description, company, location, salary_range,
                        posted_date, source_url, domain, status
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'active')
                """, (
                    job_data.get('title'),
                    job_data.get('description'),
                    job_data.get('company'),
                    job_data.get('location'),
                    job_data.get('salary'),
                    job_data.get('posted_date', datetime.now()),
                    job_data.get('url'),
                    domain
                ))
                inserted += 1
            except:
                continue  # Skip duplicates

        return jsonify({
            'success': True,
            'message': f'Discovered and added {inserted} new jobs',
            'inserted': inserted
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
