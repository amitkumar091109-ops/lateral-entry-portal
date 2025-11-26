#!/usr/bin/env python3
"""
Add 2023 Batch Appointees to Lateral Entry Database
Inserts 27 new appointees from the 3rd phase (2023) of lateral recruitment
Source: Lok Sabha Question 3831, December 2024
"""

import sqlite3
import sys
from datetime import datetime

# Database path
DB_PATH = "/home/ubuntu/projects/lateral-entry-portal/database/lateral_entry.db"

# 27 appointees from 2023 batch (3rd phase)
APPOINTEES_2023 = [
    (
        "Aashima Bhatnagar",
        "Deputy Secretary",
        "Health & Family Welfare",
        "Ministry of Health & Family Welfare",
    ),
    (
        "Ajay Kumar Arora",
        "Joint Secretary",
        "Legal Affairs",
        "Ministry of Law and Justice",
    ),
    ("G Sarathy Raja", "Deputy Secretary", "Steel", "Ministry of Steel"),
    (
        "Hardik Sheth",
        "Director",
        "Financial Services",
        "Department of Financial Services",
    ),
    (
        "Harikumar Janakiraman",
        "Director",
        "School Education & Literacy",
        "Ministry of Education",
    ),
    (
        "Himanshu Joshi",
        "Deputy Secretary",
        "Statistics & Programme Implementation",
        "Ministry of Statistics and Programme Implementation",
    ),
    ("Hitendra Sahu", "Director", "Pharmaceuticals", "Department of Pharmaceuticals"),
    (
        "Indranil Das",
        "Director",
        "Health and Family Welfare",
        "Ministry of Health and Family Welfare",
    ),
    (
        "Jigneshkumar Pareshbhai Solanki",
        "Director",
        "Financial Services",
        "Department of Financial Services",
    ),
    (
        "Madhu Sudana Sankar",
        "Joint Secretary",
        "Civil Aviation",
        "Ministry of Civil Aviation",
    ),
    (
        "Manish Kumar",
        "Deputy Secretary",
        "Heavy Industries",
        "Ministry of Heavy Industries",
    ),
    ("Manish Mishra", "Director", "Power", "Ministry of Power"),
    (
        "Manoj Muttathil",
        "Joint Secretary",
        "Financial Services",
        "Department of Financial Services",
    ),
    (
        "Minal Soni",
        "Deputy Secretary",
        "Statistics & Programme Implementation",
        "Ministry of Statistics and Programme Implementation",
    ),
    (
        "Neeraj Prakash",
        "Director",
        "Statistics & Programme Implementation",
        "Ministry of Statistics and Programme Implementation",
    ),
    (
        "Priya Jacob",
        "Director",
        "Food and Public Distribution",
        "Department of Food and Public Distribution",
    ),
    (
        "Rajeshwari S Mallegowda",
        "Director",
        "Rural Development",
        "Ministry of Rural Development",
    ),
    (
        "Ravi Ranjan Singh",
        "Director",
        "Agriculture & Farmers Welfare",
        "Ministry of Agriculture & Farmers Welfare",
    ),
    (
        "Rohina Gupta",
        "Director",
        "Housing and Urban Affairs",
        "Ministry of Housing and Urban Affairs",
    ),
    (
        "Sanjeev Kumar",
        "Deputy Secretary",
        "Statistics & Programme Implementation",
        "Ministry of Statistics and Programme Implementation",
    ),
    (
        "Santosh WB",
        "Director",
        "Chemicals and Petrochemicals",
        "Department of Chemicals and Petrochemicals",
    ),
    ("Saumya Rajan", "Deputy Secretary", "Higher Education", "Ministry of Education"),
    (
        "Sharad Kumar Dwivedi",
        "Director",
        "Agriculture & Farmers Welfare",
        "Ministry of Agriculture & Farmers Welfare",
    ),
    (
        "Shubhankit Srivastava",
        "Deputy Secretary",
        "Heavy Industries",
        "Ministry of Heavy Industries",
    ),
    (
        "Simrat Kaur",
        "Director",
        "Department for Promotion of Industry & Internal Trade",
        "Ministry of Commerce and Industry",
    ),
    ("Sunil Kumar Sharma", "Director", "Power", "Ministry of Power"),
    (
        "Vishnu Mishra",
        "Director",
        "Statistics & Programme Implementation",
        "Ministry of Statistics and Programme Implementation",
    ),
]


def add_2023_batch():
    """Add 27 appointees from 2023 batch to database"""
    conn = None
    try:
        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Prepare insert statement
        insert_sql = """
        INSERT INTO lateral_entrants 
        (name, batch_year, position, department, ministry, verified_source, current_status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        verified_source = (
            "Lok Sabha Unstarred Question No. 3831 (18.12.2024) - Annexure-I"
        )
        current_status = "Active"

        # Insert each appointee
        inserted_count = 0
        for name, position, department, ministry in APPOINTEES_2023:
            try:
                cursor.execute(
                    insert_sql,
                    (
                        name,
                        2023,
                        position,
                        department,
                        ministry,
                        verified_source,
                        current_status,
                    ),
                )
                inserted_count += 1
                print(f"✓ Added: {name} - {position} - {department}")
            except sqlite3.IntegrityError as e:
                print(f"⚠ Skipped (duplicate): {name}")
            except Exception as e:
                print(f"✗ Error adding {name}: {e}")

        # Commit changes
        conn.commit()

        # Verify results
        cursor.execute(
            "SELECT batch_year, COUNT(*) FROM lateral_entrants GROUP BY batch_year ORDER BY batch_year"
        )
        results = cursor.fetchall()

        print("\n" + "=" * 60)
        print("DATABASE UPDATE COMPLETE")
        print("=" * 60)
        print(f"Successfully inserted: {inserted_count} appointees")
        print("\nBatch Distribution:")
        for batch, count in results:
            print(f"  Batch {batch}: {count} appointees")

        cursor.execute("SELECT COUNT(*) FROM lateral_entrants")
        total = cursor.fetchone()[0]
        print(f"\nTotal Records: {total}")
        print("=" * 60)

        return True

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print("ADDING 2023 BATCH TO LATERAL ENTRY DATABASE")
    print("=" * 60)
    print(f"Database: {DB_PATH}")
    print(f"Appointees to add: {len(APPOINTEES_2023)}")
    print(f"Batch year: 2023")
    print("=" * 60 + "\n")

    success = add_2023_batch()
    sys.exit(0 if success else 1)
