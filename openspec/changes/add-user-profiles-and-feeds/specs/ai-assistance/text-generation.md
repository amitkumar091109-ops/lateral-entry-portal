# Capability Spec: AI Text Assistance

**Feature**: `ai-text-assistance`  
**Parent Change**: `add-user-profiles-and-feeds`  
**Status**: Draft

## Overview

Integrate a custom AI model to assist users in writing professional profile content. Users provide bullet points or rough text, and the AI generates polished, professional descriptions suitable for government profiles.

## Requirements

### Functional Requirements

1. **AI Suggestion Generation**:
   - User clicks "AI Assist" button next to text field
   - User's existing data sent to AI model
   - AI generates professional text suggestion
   - User reviews suggestion in modal
   - User can edit AI suggestion before accepting
   - User can reject and write manually

2. **Content Types**:
   - Profile summary (from name, position, education, experience)
   - Achievement descriptions (from bullet points)
   - Professional experience (from work history)
   - Education descriptions (from degree details)
   - Grammar and style improvements for existing text

3. **AI Usage Tracking**:
   - Track number of requests per user
   - Rate limiting (configurable per user tier)
   - Log AI suggestions for quality monitoring
   - Show usage stats to users and admins

4. **Fallback Mechanism**:
   - If AI unavailable, show template-based suggestions
   - Clear error messages when AI fails
   - Manual entry always available

### Non-Functional Requirements

1. **Performance**:
   - AI response in < 5 seconds
   - Timeout after 10 seconds with fallback
   - Async requests don't block UI

2. **Reliability**:
   - Handle AI service downtime gracefully
   - Retry logic for transient failures (3 attempts)
   - Fallback to templates if AI consistently fails

3. **Cost Control**:
   - Rate limiting prevents abuse
   - Default: 10 requests/hour, 50 requests/day per user
   - Admin configurable limits

## Technical Specification

### API Endpoints

```
POST /api/ai/suggest-summary      - Generate profile summary
POST /api/ai/suggest-achievement  - Generate achievement text
POST /api/ai/improve-text         - Improve existing text
GET  /api/ai/usage                - Get usage stats for current user
GET  /api/admin/ai/usage          - Get system-wide AI usage (admin)
```

### Request/Response Format

```json
// POST /api/ai/suggest-summary
{
  "name": "Jane Doe",
  "position": "Joint Secretary",
  "ministry": "Ministry of Finance",
  "education": "MBA from IIM Bangalore",
  "experience": "15 years in banking sector"
}

// Response
{
  "success": true,
  "source": "ai",
  "suggestion": "Jane Doe serves as Joint Secretary...",
  "word_count": 187,
  "tokens_used": 245,
  "model_version": "gpt-4",
  "confidence": 0.92
}

// POST /api/ai/suggest-achievement
{
  "achievement_type": "project",
  "bullet_points": [
    "Led digital transformation initiative",
    "Reduced processing time by 60%",
    "Trained 200+ staff members"
  ]
}

// Response
{
  "success": true,
  "source": "ai",
  "suggestion": "Spearheaded a comprehensive digital transformation initiative...",
  "word_count": 98,
  "tokens_used": 156
}

// POST /api/ai/improve-text
{
  "text": "I have work in many project and achieve good result.",
  "improvement_type": "grammar" // grammar, style, concise, professional
}

// Response
{
  "success": true,
  "original": "I have work in many project...",
  "improved": "I have worked on numerous projects and achieved excellent results.",
  "changes": [
    {"type": "grammar", "from": "have work", "to": "have worked"},
    {"type": "word_choice", "from": "many project", "to": "numerous projects"}
  ]
}

// Error response (AI unavailable)
{
  "success": false,
  "source": "template",
  "error": "AI service temporarily unavailable",
  "suggestion": "<template-based text>",
  "fallback": true
}
```

### Database Schema

```sql
-- AI suggestion history
CREATE TABLE ai_suggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    content_type VARCHAR(100), -- summary, achievement, education, improvement
    input_data TEXT,
    generated_content TEXT,
    was_accepted BOOLEAN,
    edited_content TEXT,
    model_version VARCHAR(100),
    tokens_used INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- AI usage tracking
CREATE TABLE ai_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    request_type VARCHAR(100),
    tokens_used INTEGER,
    response_time_ms INTEGER,
    success BOOLEAN,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_ai_usage_user_date ON ai_usage(user_id, created_at);
```

### Configuration

```bash
# Custom AI Model
CUSTOM_AI_BASE_URL=<user-provides>
CUSTOM_AI_API_KEY=<user-provides>
CUSTOM_AI_MODEL=<user-provides>

# Rate Limits (requests per time period)
AI_RATE_LIMIT_PER_HOUR=10
AI_RATE_LIMIT_PER_DAY=50
AI_REQUEST_TIMEOUT=10  # seconds

# Fallback settings
AI_ENABLE_FALLBACK=true
AI_RETRY_ATTEMPTS=3
AI_RETRY_DELAY=1  # seconds
```

## User Interface

### AI Assist Button

```html
<div class="field-group">
    <label for="profile-summary">Profile Summary</label>
    <textarea id="profile-summary" 
              data-ai-assist="summary" 
              data-word-limit="profile_summary"
              rows="6"></textarea>
    
    <div class="field-actions">
        <button class="ai-assist-btn" onclick="showAISuggestion('summary')">
            <i class="fas fa-magic"></i> AI Assist
        </button>
        <div class="word-counter">0 / 200 words</div>
    </div>
</div>
```

### AI Suggestion Modal

```html
<div class="modal ai-suggestion-modal">
    <h2><i class="fas fa-magic"></i> AI Suggestion</h2>
    
    <div class="suggestion-container">
        <div class="current-section">
            <h3>Your Current Text:</h3>
            <div class="current-text">
                <em>No text yet</em>
            </div>
        </div>
        
        <div class="divider"></div>
        
        <div class="suggested-section">
            <h3>AI Suggested Text:</h3>
            <div class="suggested-text" contenteditable="true">
                <!-- AI generated text appears here -->
            </div>
            <p class="suggestion-info">
                <i class="fas fa-info-circle"></i>
                You can edit this suggestion before using it.
            </p>
        </div>
    </div>
    
    <div class="modal-actions">
        <button class="btn-primary" onclick="acceptSuggestion()">
            Use This Text
        </button>
        <button class="btn-secondary" onclick="regenerate()">
            <i class="fas fa-redo"></i> Regenerate
        </button>
        <button class="btn-tertiary" onclick="closeModal()">
            Cancel
        </button>
    </div>
    
    <div class="usage-info">
        <p>AI requests remaining today: <strong id="remaining-requests">42</strong></p>
    </div>
</div>
```

### Loading State

```html
<div class="ai-loading">
    <div class="spinner"></div>
    <p>AI is generating your text...</p>
    <small>This usually takes 3-5 seconds</small>
</div>
```

## Backend Implementation

### AI Service Class

```python
# ai_service.py

import httpx
import time
from typing import Dict, Optional

class AIService:
    def __init__(self, config):
        self.base_url = config['CUSTOM_AI_BASE_URL']
        self.api_key = config['CUSTOM_AI_API_KEY']
        self.model = config.get('CUSTOM_AI_MODEL', 'default')
        self.timeout = config.get('AI_REQUEST_TIMEOUT', 10)
        self.rate_limiter = AIRateLimiter(config)
    
    async def suggest_summary(self, user_data: Dict) -> Dict:
        """Generate profile summary from user data"""
        
        # Check rate limit
        if not self.rate_limiter.allow_request(user_data['user_id']):
            raise RateLimitExceeded("Daily AI request limit reached")
        
        # Build prompt
        prompt = self._build_summary_prompt(user_data)
        
        # Call AI API
        start_time = time.time()
        try:
            response = await self._call_ai_api(prompt, 'summary')
            response_time = int((time.time() - start_time) * 1000)
            
            # Log usage
            self._log_usage(
                user_id=user_data['user_id'],
                request_type='summary',
                tokens_used=response.get('tokens_used', 0),
                response_time_ms=response_time,
                success=True
            )
            
            return {
                'success': True,
                'source': 'ai',
                'suggestion': response['text'],
                'word_count': len(response['text'].split()),
                'tokens_used': response.get('tokens_used', 0),
                'model_version': self.model
            }
            
        except Exception as e:
            response_time = int((time.time() - start_time) * 1000)
            self._log_usage(
                user_id=user_data['user_id'],
                request_type='summary',
                response_time_ms=response_time,
                success=False,
                error_message=str(e)
            )
            
            # Fall back to template
            return self._fallback_template(user_data, 'summary')
    
    async def _call_ai_api(self, prompt: str, request_type: str) -> Dict:
        """Make API call to custom AI model"""
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': self.model,
            'prompt': prompt,
            'max_tokens': 500,
            'temperature': 0.7
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f'{self.base_url}/generate',
                    json=payload,
                    headers=headers,
                    timeout=self.timeout
                )
                response.raise_for_status()
                return response.json()
                
            except httpx.TimeoutException:
                raise AIServiceError("AI request timed out")
            except httpx.HTTPStatusError as e:
                raise AIServiceError(f"AI API error: {e.response.status_code}")
    
    def _build_summary_prompt(self, user_data: Dict) -> str:
        """Build prompt for summary generation"""
        return f"""
Generate a professional 2-3 paragraph summary for a government lateral entry appointee profile.

Name: {user_data['name']}
Position: {user_data['position']}
Ministry: {user_data['ministry']}
Education: {user_data.get('education', 'Not provided')}
Previous Experience: {user_data.get('experience', 'Not provided')}

Requirements:
- Professional tone appropriate for government website
- Highlight relevant expertise and contributions
- 150-200 words
- Focus on qualifications and impact
- Avoid jargon and overly technical language
- Write in third person

Generate only the summary text, nothing else.
"""
    
    def _fallback_template(self, user_data: Dict, content_type: str) -> Dict:
        """Generate template-based suggestion when AI fails"""
        templates = {
            'summary': f"{user_data['name']} serves as {user_data['position']} "
                      f"in the {user_data['ministry']}. With extensive experience "
                      f"in their field, they bring valuable expertise to their role."
        }
        
        return {
            'success': True,
            'source': 'template',
            'suggestion': templates.get(content_type, ''),
            'fallback': True,
            'error': 'AI service unavailable, using template'
        }
```

### Rate Limiter

```python
# ai_rate_limiter.py

from datetime import datetime, timedelta
from collections import defaultdict

class AIRateLimiter:
    def __init__(self, config):
        self.hourly_limit = config.get('AI_RATE_LIMIT_PER_HOUR', 10)
        self.daily_limit = config.get('AI_RATE_LIMIT_PER_DAY', 50)
        self.requests = defaultdict(list)
    
    def allow_request(self, user_id: int) -> bool:
        """Check if user can make another AI request"""
        now = datetime.now()
        
        # Get user's recent requests
        user_requests = self._get_user_requests(user_id, now)
        
        # Check hourly limit
        hour_ago = now - timedelta(hours=1)
        hourly_count = sum(1 for req_time in user_requests if req_time > hour_ago)
        if hourly_count >= self.hourly_limit:
            return False
        
        # Check daily limit
        day_ago = now - timedelta(days=1)
        daily_count = sum(1 for req_time in user_requests if req_time > day_ago)
        if daily_count >= self.daily_limit:
            return False
        
        # Record request
        self.requests[user_id].append(now)
        return True
    
    def get_remaining_requests(self, user_id: int) -> Dict[str, int]:
        """Get remaining requests for user"""
        now = datetime.now()
        user_requests = self._get_user_requests(user_id, now)
        
        hour_ago = now - timedelta(hours=1)
        day_ago = now - timedelta(days=1)
        
        hourly_used = sum(1 for req_time in user_requests if req_time > hour_ago)
        daily_used = sum(1 for req_time in user_requests if req_time > day_ago)
        
        return {
            'hourly_remaining': max(0, self.hourly_limit - hourly_used),
            'daily_remaining': max(0, self.daily_limit - daily_used)
        }
```

## Prompt Templates

See `design.md` for detailed prompt templates for each content type.

## Security Considerations

1. **API Key Protection**: Store AI API key encrypted
2. **Rate Limiting**: Prevent abuse of AI service
3. **Input Validation**: Sanitize user input before sending to AI
4. **Output Validation**: Check AI responses for inappropriate content
5. **Cost Control**: Monitor token usage and set budgets

## Testing Strategy

### Test Cases

1. **Successful Generation**: AI returns valid suggestion
2. **Timeout Handling**: Request times out, fallback triggered
3. **Rate Limit**: User exceeds limit, clear error shown
4. **Fallback**: AI unavailable, template suggestion shown
5. **Edit Suggestion**: User edits AI text before accepting
6. **Reject Suggestion**: User rejects and writes manually

## Success Criteria

- [ ] AI generates helpful suggestions < 5 seconds
- [ ] Rate limiting prevents abuse
- [ ] Fallback works when AI unavailable
- [ ] Users can edit suggestions before accepting
- [ ] Usage tracking works correctly
- [ ] No inappropriate content generated
- [ ] Error messages are clear and helpful

## Related Specs

- [Profile Editing](../moderation/text-moderation.md)
- [Admin Settings](../admin-panel/settings.md)
