#!/usr/bin/env python3
"""
Export Static JSON Files for Lateral Entry Portal Deployment
Creates entrants.json, stats.json, and batches.json for static deployment
"""

import sqlite3
import json
from pathlib import Path

DB_PATH = "/home/ubuntu/projects/lateral-entry-portal/database/lateral_entry.db"
OUTPUT_DIR = Path("/home/ubuntu/projects/lateral-entry-portal/data")


def export_entrants():
    """Export all entrants to JSON"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, batch_year, position, department, ministry, 
               state, profile_summary, educational_background, 
               previous_experience, date_of_appointment, current_status, 
               verified_source
        FROM lateral_entrants
        ORDER BY batch_year DESC, name ASC
    """)

    entrants = [dict(row) for row in cursor.fetchall()]
    conn.close()

    output_file = OUTPUT_DIR / "entrants.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(entrants, f, indent=2, ensure_ascii=False)

    print(f"✓ Exported {len(entrants)} entrants to {output_file}")
    return len(entrants)


def export_stats():
    """Export statistics to JSON"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    stats = {}

    # Total appointees
    cursor.execute("SELECT COUNT(*) as total FROM lateral_entrants")
    stats["total_appointees"] = cursor.fetchone()["total"]

    # By batch
    cursor.execute("""
        SELECT batch_year, COUNT(*) as count 
        FROM lateral_entrants 
        GROUP BY batch_year 
        ORDER BY batch_year
    """)
    stats["by_batch"] = [dict(row) for row in cursor.fetchall()]

    # By ministry
    cursor.execute("""
        SELECT ministry, COUNT(*) as count 
        FROM lateral_entrants 
        WHERE ministry IS NOT NULL AND ministry != ''
        GROUP BY ministry 
        ORDER BY count DESC
    """)
    stats["by_ministry"] = [dict(row) for row in cursor.fetchall()]

    # By position
    cursor.execute("""
        SELECT position, COUNT(*) as count 
        FROM lateral_entrants 
        GROUP BY position 
        ORDER BY count DESC
    """)
    stats["by_position"] = [dict(row) for row in cursor.fetchall()]

    # By department
    cursor.execute("""
        SELECT department, COUNT(*) as count 
        FROM lateral_entrants 
        WHERE department IS NOT NULL AND department != ''
        GROUP BY department 
        ORDER BY count DESC
    """)
    stats["by_department"] = [dict(row) for row in cursor.fetchall()]

    conn.close()

    output_file = OUTPUT_DIR / "stats.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    print(f"✓ Exported statistics to {output_file}")
    print(f"  - Total appointees: {stats['total_appointees']}")
    print(f"  - Batches: {len(stats['by_batch'])}")
    print(f"  - Ministries: {len(stats['by_ministry'])}")
    print(f"  - Positions: {len(stats['by_position'])}")

    return stats


def export_batches():
    """Export batch information to JSON"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT batch_year, COUNT(*) as count 
        FROM lateral_entrants 
        GROUP BY batch_year 
        ORDER BY batch_year
    """)

    batches = [dict(row) for row in cursor.fetchall()]

    # Add batch metadata
    batch_metadata = {
        2019: {
            "advertisement": "Advertisement No. 17/2018",
            "phase": "1st Phase (2018)",
            "description": "Pioneer batch of lateral entry appointees",
        },
        2021: {
            "advertisement": "Advertisement No. 47/2020",
            "phase": "2nd Phase (2021)",
            "description": "Largest cohort of lateral entry appointments",
        },
        2023: {
            "advertisement": "Advertisement No. 52 & 53/2023",
            "phase": "3rd Phase (2023)",
            "description": "Third phase of lateral entry appointments",
        },
    }

    for batch in batches:
        year = batch["batch_year"]
        if year in batch_metadata:
            batch.update(batch_metadata[year])

    conn.close()

    output_file = OUTPUT_DIR / "batches.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(batches, f, indent=2, ensure_ascii=False)

    print(f"✓ Exported batch information to {output_file}")
    for batch in batches:
        print(f"  - {batch['batch_year']}: {batch['count']} appointees")

    return batches


def main():
    print("=" * 60)
    print("EXPORTING STATIC JSON FILES FOR DEPLOYMENT")
    print("=" * 60)
    print()

    # Create output directory if it doesn't exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Export all data
    total = export_entrants()
    print()
    stats = export_stats()
    print()
    batches = export_batches()

    print()
    print("=" * 60)
    print("EXPORT COMPLETE")
    print("=" * 60)
    print(f"Files created in: {OUTPUT_DIR}")
    print("- entrants.json")
    print("- stats.json")
    print("- batches.json")
    print()
    print("Ready for deployment!")


if __name__ == "__main__":
    main()
