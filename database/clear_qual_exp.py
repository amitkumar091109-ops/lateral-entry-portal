#!/usr/bin/env python3
"""
Clear qualification and experience data from all lateral entrants
Sets educational_background and previous_experience to NULL
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "lateral_entry.db")

def clear_qualification_experience():
    """Set educational_background and previous_experience to NULL for all entrants"""
    
    print("Clearing qualification and experience data...")
    print(f"Database: {DB_PATH}")
    print("=" * 70)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check current state
        cursor.execute("""
            SELECT COUNT(*) as total,
                   COUNT(educational_background) as with_edu,
                   COUNT(previous_experience) as with_exp
            FROM lateral_entrants
        """)
        before = cursor.fetchone()
        print(f"\nBEFORE:")
        print(f"  Total entrants: {before[0]}")
        print(f"  With educational_background: {before[1]}")
        print(f"  With previous_experience: {before[2]}")
        
        # Update to NULL
        cursor.execute("""
            UPDATE lateral_entrants 
            SET educational_background = NULL,
                previous_experience = NULL,
                updated_at = CURRENT_TIMESTAMP
        """)
        
        rows_affected = cursor.rowcount
        conn.commit()
        
        # Check after state
        cursor.execute("""
            SELECT COUNT(*) as total,
                   COUNT(educational_background) as with_edu,
                   COUNT(previous_experience) as with_exp
            FROM lateral_entrants
        """)
        after = cursor.fetchone()
        
        print(f"\nAFTER:")
        print(f"  Total entrants: {after[0]}")
        print(f"  With educational_background: {after[1]}")
        print(f"  With previous_experience: {after[2]}")
        print(f"\nRows updated: {rows_affected}")
        print("=" * 70)
        print("✓ Successfully cleared qualification and experience data")
        
    except Exception as e:
        conn.rollback()
        print(f"✗ Error: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    clear_qualification_experience()
