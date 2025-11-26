"""
Flask API Server for Lateral Entry Portal
Provides RESTful endpoints for all portal data
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "database", "lateral_entry.db"
)


def get_db():
    """Create database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn


def dict_from_row(row):
    """Convert sqlite3.Row to dictionary"""
    return dict(zip(row.keys(), row)) if row else None


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify(
        {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "database": os.path.exists(DB_PATH),
        }
    )


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Get comprehensive portal statistics"""
    conn = get_db()
    cursor = conn.cursor()

    # Total count
    cursor.execute("SELECT COUNT(*) as total FROM lateral_entrants")
    total = cursor.fetchone()["total"]

    # By batch
    cursor.execute("""
        SELECT batch_year, COUNT(*) as count 
        FROM lateral_entrants 
        GROUP BY batch_year 
        ORDER BY batch_year
    """)
    by_batch = [dict_from_row(row) for row in cursor.fetchall()]

    # By position
    cursor.execute("""
        SELECT position, COUNT(*) as count 
        FROM lateral_entrants 
        GROUP BY position 
        ORDER BY count DESC
    """)
    by_position = [dict_from_row(row) for row in cursor.fetchall()]

    # By ministry (all ministries)
    cursor.execute("""
        SELECT ministry, COUNT(*) as count 
        FROM lateral_entrants 
        WHERE ministry IS NOT NULL
        GROUP BY ministry 
        ORDER BY count DESC
    """)
    by_ministry = [dict_from_row(row) for row in cursor.fetchall()]

    # Count distinct ministries
    cursor.execute(
        "SELECT COUNT(DISTINCT ministry) as count FROM lateral_entrants WHERE ministry IS NOT NULL"
    )
    ministry_count = cursor.fetchone()["count"]

    # Recent appointments (last 10)
    cursor.execute("""
        SELECT name, position, ministry, date_of_appointment
        FROM lateral_entrants 
        ORDER BY date_of_appointment DESC 
        LIMIT 10
    """)
    recent = [dict_from_row(row) for row in cursor.fetchall()]

    conn.close()

    return jsonify(
        {
            "total_appointees": total,
            "total_ministries": ministry_count,
            "total_positions": len(by_position),
            "total_batches": len(by_batch),
            "by_batch": by_batch,
            "by_position": by_position,
            "by_ministry": by_ministry,
            "recent_appointments": recent,
            "last_updated": datetime.now().isoformat(),
        }
    )


@app.route("/api/entrants", methods=["GET"])
def get_entrants():
    """
    Get all lateral entrants with optional filters
    Query params: batch_year, position, ministry, limit, offset
    """
    conn = get_db()
    cursor = conn.cursor()

    # Build query with filters
    query = "SELECT * FROM lateral_entrants WHERE 1=1"
    params = []

    if request.args.get("batch_year"):
        query += " AND batch_year = ?"
        params.append(request.args.get("batch_year"))

    if request.args.get("position"):
        query += " AND position = ?"
        params.append(request.args.get("position"))

    if request.args.get("ministry"):
        query += " AND ministry LIKE ?"
        params.append(f"%{request.args.get('ministry')}%")

    # Search by name
    if request.args.get("search"):
        query += " AND name LIKE ?"
        params.append(f"%{request.args.get('search')}%")

    # Add ordering
    query += " ORDER BY batch_year DESC, date_of_appointment DESC"

    # Add pagination
    limit = int(request.args.get("limit", 50))
    offset = int(request.args.get("offset", 0))
    query += f" LIMIT {limit} OFFSET {offset}"

    cursor.execute(query, params)
    entrants = [dict_from_row(row) for row in cursor.fetchall()]

    # Get total count for pagination
    count_query = "SELECT COUNT(*) as total FROM lateral_entrants WHERE 1=1"
    if request.args.get("batch_year"):
        count_query += " AND batch_year = ?"
    if request.args.get("position"):
        count_query += " AND position = ?"
    if request.args.get("ministry"):
        count_query += " AND ministry LIKE ?"
    if request.args.get("search"):
        count_query += " AND name LIKE ?"

    cursor.execute(count_query, params)
    total = cursor.fetchone()["total"]

    conn.close()

    return jsonify(
        {
            "entrants": entrants,
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": (offset + limit) < total,
        }
    )


@app.route("/api/entrants/<int:entrant_id>", methods=["GET"])
def get_entrant(entrant_id):
    """Get detailed information for a specific entrant"""
    conn = get_db()
    cursor = conn.cursor()

    # Get basic info
    cursor.execute("SELECT * FROM lateral_entrants WHERE id = ?", (entrant_id,))
    entrant = dict_from_row(cursor.fetchone())

    if not entrant:
        conn.close()
        return jsonify({"error": "Entrant not found"}), 404

    # Get professional details
    cursor.execute(
        "SELECT * FROM professional_details WHERE entrant_id = ?", (entrant_id,)
    )
    professional = [dict_from_row(row) for row in cursor.fetchall()]

    # Get education details
    cursor.execute(
        "SELECT * FROM education_details WHERE entrant_id = ?", (entrant_id,)
    )
    education = [dict_from_row(row) for row in cursor.fetchall()]

    # Get media coverage
    cursor.execute(
        "SELECT * FROM media_coverage WHERE entrant_id = ? ORDER BY publication_date DESC",
        (entrant_id,),
    )
    media = [dict_from_row(row) for row in cursor.fetchall()]

    # Get achievements
    cursor.execute("SELECT * FROM achievements WHERE entrant_id = ?", (entrant_id,))
    achievements = [dict_from_row(row) for row in cursor.fetchall()]

    conn.close()

    entrant["professional_details"] = professional
    entrant["education"] = education
    entrant["media_coverage"] = media
    entrant["achievements"] = achievements

    return jsonify(entrant)


@app.route("/api/batches", methods=["GET"])
def get_batches():
    """Get summary of all batches"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            batch_year,
            COUNT(*) as total_appointees,
            COUNT(DISTINCT position) as positions_filled,
            COUNT(DISTINCT ministry) as ministries_involved,
            MIN(date_of_appointment) as first_appointment,
            MAX(date_of_appointment) as last_appointment
        FROM lateral_entrants
        GROUP BY batch_year
        ORDER BY batch_year
    """)

    batches = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()

    return jsonify({"batches": batches})


@app.route("/api/batches/<int:batch_year>", methods=["GET"])
def get_batch_detail(batch_year):
    """Get detailed information for a specific batch"""
    conn = get_db()
    cursor = conn.cursor()

    # Get all entrants in batch
    cursor.execute(
        """
        SELECT * FROM lateral_entrants 
        WHERE batch_year = ? 
        ORDER BY position, name
    """,
        (batch_year,),
    )
    entrants = [dict_from_row(row) for row in cursor.fetchall()]

    if not entrants:
        conn.close()
        return jsonify({"error": "Batch not found"}), 404

    # Get batch statistics
    cursor.execute(
        """
        SELECT 
            COUNT(*) as total,
            COUNT(DISTINCT position) as positions,
            COUNT(DISTINCT ministry) as ministries
        FROM lateral_entrants
        WHERE batch_year = ?
    """,
        (batch_year,),
    )
    stats = dict_from_row(cursor.fetchone())

    # Group by position
    cursor.execute(
        """
        SELECT position, COUNT(*) as count
        FROM lateral_entrants
        WHERE batch_year = ?
        GROUP BY position
        ORDER BY count DESC
    """,
        (batch_year,),
    )
    by_position = [dict_from_row(row) for row in cursor.fetchall()]

    conn.close()

    return jsonify(
        {
            "batch_year": batch_year,
            "statistics": stats,
            "by_position": by_position,
            "entrants": entrants,
        }
    )


@app.route("/api/ministries", methods=["GET"])
def get_ministries():
    """Get list of all ministries with appointee counts"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            ministry,
            COUNT(*) as appointee_count,
            GROUP_CONCAT(DISTINCT position) as positions
        FROM lateral_entrants
        GROUP BY ministry
        ORDER BY appointee_count DESC
    """)

    ministries = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()

    return jsonify({"ministries": ministries})


@app.route("/api/positions", methods=["GET"])
def get_positions():
    """Get list of all positions with counts"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            position,
            COUNT(*) as count,
            GROUP_CONCAT(DISTINCT batch_year) as batches
        FROM lateral_entrants
        GROUP BY position
        ORDER BY count DESC
    """)

    positions = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()

    return jsonify({"positions": positions})


@app.route("/api/search", methods=["GET"])
def search():
    """
    Search across all entrants
    Query params: q (search term), fields (comma-separated: name,ministry,department,position)
    """
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": 'Query parameter "q" is required'}), 400

    fields = request.args.get("fields", "name,ministry,department,position").split(",")

    conn = get_db()
    cursor = conn.cursor()

    # Build search query
    conditions = []
    params = []
    for field in fields:
        if field in ["name", "ministry", "department", "position"]:
            conditions.append(f"{field} LIKE ?")
            params.append(f"%{query}%")

    if not conditions:
        conn.close()
        return jsonify({"error": "Invalid search fields"}), 400

    search_query = f"""
        SELECT * FROM lateral_entrants
        WHERE {" OR ".join(conditions)}
        ORDER BY batch_year DESC
    """

    cursor.execute(search_query, params)
    results = [dict_from_row(row) for row in cursor.fetchall()]

    conn.close()

    return jsonify({"query": query, "results": results, "count": len(results)})


@app.route("/api/export", methods=["GET"])
def export_data():
    """
    Export data in various formats
    Query param: format (json, csv)
    """
    export_format = request.args.get("format", "json")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM lateral_entrants ORDER BY batch_year, name")
    entrants = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()

    if export_format == "csv":
        # Convert to CSV format
        import io
        import csv

        output = io.StringIO()
        if entrants:
            writer = csv.DictWriter(output, fieldnames=entrants[0].keys())
            writer.writeheader()
            writer.writerows(entrants)

        response = app.response_class(
            response=output.getvalue(),
            mimetype="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=lateral_entrants.csv"
            },
        )
        return response

    # Default: JSON
    return jsonify(
        {
            "data": entrants,
            "count": len(entrants),
            "exported_at": datetime.now().isoformat(),
        }
    )


@app.route("/api/timeline", methods=["GET"])
def get_timeline():
    """Get chronological timeline of all appointments"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            date_of_appointment,
            batch_year,
            COUNT(*) as count,
            GROUP_CONCAT(name) as names
        FROM lateral_entrants
        WHERE date_of_appointment IS NOT NULL
        GROUP BY date_of_appointment, batch_year
        ORDER BY date_of_appointment
    """)

    timeline = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()

    return jsonify({"timeline": timeline})


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    print("=" * 70)
    print("LATERAL ENTRY PORTAL API SERVER")
    print("=" * 70)
    print(f"Database: {DB_PATH}")
    print(f"Database exists: {os.path.exists(DB_PATH)}")
    print("=" * 70)
    print("\nAvailable endpoints:")
    print("  GET  /api/health              - Health check")
    print("  GET  /api/stats               - Portal statistics")
    print("  GET  /api/entrants            - List all entrants (with filters)")
    print("  GET  /api/entrants/<id>       - Get entrant details")
    print("  GET  /api/batches             - List all batches")
    print("  GET  /api/batches/<year>      - Get batch details")
    print("  GET  /api/ministries          - List all ministries")
    print("  GET  /api/positions           - List all positions")
    print("  GET  /api/search?q=<query>    - Search entrants")
    print("  GET  /api/export?format=csv   - Export data")
    print("  GET  /api/timeline            - Appointment timeline")
    print("=" * 70)
    print("\nStarting server on http://localhost:5000")
    print("=" * 70 + "\n")

    app.run(debug=True, host="0.0.0.0", port=5000)
