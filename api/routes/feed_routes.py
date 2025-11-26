"""
Social Feed and News Routes
API endpoints for social media feeds and news monitoring
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import httpx

from ..database import db, row_to_dict
from ..auth.decorators import optional_auth
from ..config import get_config

config = get_config()

feed_bp = Blueprint('feed', __name__, url_prefix='/api/feed')


class FeedMonitoringService:
    """Monitor social media and news using Parallel AI"""

    def __init__(self):
        self.api_key = config.PARALLEL_AI_API_KEY
        self.api_url = config.PARALLEL_AI_API_URL or "https://api.parallelai.com/v1"

    async def fetch_social_posts(self, keywords: list, platforms: list = None) -> list:
        """Fetch social media posts"""
        if not self.api_key:
            return []

        platforms = platforms or ['twitter', 'linkedin']

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/social/search",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "keywords": keywords,
                    "platforms": platforms,
                    "max_results": 50
                },
                timeout=60.0
            )

            if response.status_code != 200:
                return []

            data = response.json()
            return data.get('posts', [])

    async def fetch_news_articles(self, query: str, days_back: int = 7) -> list:
        """Fetch news articles"""
        if not self.api_key:
            return []

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/news/search",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "query": query,
                    "days_back": days_back,
                    "max_results": 100
                },
                timeout=60.0
            )

            if response.status_code != 200:
                return []

            data = response.json()
            return data.get('articles', [])


feed_service = FeedMonitoringService()


# ============================================================================
# Social Feed
# ============================================================================

@feed_bp.route('/social', methods=['GET'])
@optional_auth
def get_social_feed():
    """Get social media posts"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        platform = request.args.get('platform', '')

        offset = (page - 1) * per_page

        # Build query
        where_clause = "1=1"
        params = []

        if platform:
            where_clause += " AND platform = ?"
            params.append(platform)

        # Get total count
        count_query = f"SELECT COUNT(*) as count FROM social_feed_items WHERE {where_clause}"
        count_result = db.execute_one(count_query, params)
        total = count_result['count'] if count_result else 0

        # Get posts
        query = f"""
            SELECT * FROM social_feed_items
            WHERE {where_clause}
            ORDER BY posted_at DESC
            LIMIT ? OFFSET ?
        """
        params.extend([per_page, offset])
        posts = db.execute(query, params)

        return jsonify({
            'success': True,
            'posts': [row_to_dict(p) for p in posts],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@feed_bp.route('/social/refresh', methods=['POST'])
async def refresh_social_feed():
    """Refresh social media feed (admin or scheduled)"""
    try:
        # Fetch latest posts
        keywords = ['lateral entry', 'government jobs', 'civil service']
        posts = await feed_service.fetch_social_posts(keywords)

        # Store in database
        inserted = 0
        for post_data in posts:
            try:
                # Check if post already exists
                existing = db.execute_one("""
                    SELECT id FROM social_feed_items WHERE external_id = ?
                """, (post_data.get('id'),))

                if not existing:
                    db.insert("""
                        INSERT INTO social_feed_items (
                            platform, external_id, author, content, post_url,
                            posted_at, likes_count, shares_count
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        post_data.get('platform'),
                        post_data.get('id'),
                        post_data.get('author'),
                        post_data.get('content'),
                        post_data.get('url'),
                        post_data.get('posted_at', datetime.now()),
                        post_data.get('likes', 0),
                        post_data.get('shares', 0)
                    ))
                    inserted += 1
            except:
                continue

        return jsonify({
            'success': True,
            'message': f'Refreshed social feed, added {inserted} new posts',
            'inserted': inserted
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# News Articles
# ============================================================================

@feed_bp.route('/news', methods=['GET'])
@optional_auth
def get_news():
    """Get news articles"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        category = request.args.get('category', '')

        offset = (page - 1) * per_page

        # Build query
        where_clause = "1=1"
        params = []

        if category:
            where_clause += " AND category = ?"
            params.append(category)

        # Get total count
        count_query = f"SELECT COUNT(*) as count FROM news_articles WHERE {where_clause}"
        count_result = db.execute_one(count_query, params)
        total = count_result['count'] if count_result else 0

        # Get articles
        query = f"""
            SELECT * FROM news_articles
            WHERE {where_clause}
            ORDER BY published_at DESC
            LIMIT ? OFFSET ?
        """
        params.extend([per_page, offset])
        articles = db.execute(query, params)

        return jsonify({
            'success': True,
            'articles': [row_to_dict(a) for a in articles],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@feed_bp.route('/news/refresh', methods=['POST'])
async def refresh_news():
    """Refresh news articles (admin or scheduled)"""
    try:
        # Fetch latest news
        query = "lateral entry OR government recruitment OR civil service"
        articles = await feed_service.fetch_news_articles(query, days_back=7)

        # Store in database
        inserted = 0
        for article_data in articles:
            try:
                # Check if article already exists
                existing = db.execute_one("""
                    SELECT id FROM news_articles WHERE article_url = ?
                """, (article_data.get('url'),))

                if not existing:
                    db.insert("""
                        INSERT INTO news_articles (
                            title, summary, source, article_url, published_at, category
                        )
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        article_data.get('title'),
                        article_data.get('summary'),
                        article_data.get('source'),
                        article_data.get('url'),
                        article_data.get('published_at', datetime.now()),
                        article_data.get('category', 'general')
                    ))
                    inserted += 1
            except:
                continue

        return jsonify({
            'success': True,
            'message': f'Refreshed news feed, added {inserted} new articles',
            'inserted': inserted
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@feed_bp.route('/news/categories', methods=['GET'])
def get_news_categories():
    """Get distinct news categories"""
    try:
        categories = db.execute("""
            SELECT DISTINCT category FROM news_articles
            WHERE category IS NOT NULL
            ORDER BY category
        """)

        return jsonify({
            'success': True,
            'categories': [row['category'] for row in categories]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
