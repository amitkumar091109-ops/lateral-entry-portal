#!/usr/bin/env python3
"""
Update lateral entry database with verified information from The Secretariat article
Date: December 19, 2024
Source: https://thesecretariat.in/article/govt-extends-term-for-17-laterally-recruited-officers
"""

import sqlite3
from datetime import datetime

DB_PATH = "/home/ubuntu/projects/lateral-entry-portal/database/lateral_entry.db"

# Verified officers from The Secretariat article (Dec 19, 2024)
VERIFIED_OFFICERS = [
    {
        "name": "Balasubramanian Krishnamurthy",
        "position": "Joint Secretary",
        "department": "Department of Revenue",
        "ministry": "Ministry of Finance",
        "appointment_type": "contract",
        "extension_date": "2027-01-16",
        "original_appointment": "2022-01-16",
        "batch_year": 2022,
    },
    {
        "name": "Samuel Praveen Kumar",
        "position": "Joint Secretary",
        "department": "Department of Agriculture, Cooperation & Farmers Welfare",
        "ministry": "Ministry of Agriculture and Farmers Welfare",
        "appointment_type": "deputation",
        "extension_date": "2026-12-30",
        "original_appointment": "2021-12-30",
        "batch_year": 2021,
    },
    {
        "name": "Manish Chadha",
        "position": "Joint Secretary",
        "department": "Department of Commerce",
        "ministry": "Ministry of Commerce and Industry",
        "appointment_type": "contract",
        "extension_date": "2027-01-06",
        "original_appointment": "2022-01-06",
        "batch_year": 2022,
    },
    {
        "name": "Govind K Bansal",
        "position": "Director",
        "department": "Department of Health & Family Welfare",
        "ministry": "Ministry of Health and Family Welfare",
        "appointment_type": "contract",
        "extension_date": "2025-12-30",
        "original_appointment": "2021-12-30",
        "batch_year": 2021,
    },
    {
        "name": "Sagar Rameshrao Kadu",
        "position": "Director",
        "department": "Department for Promotion of Industry and Internal Trade",
        "ministry": "Ministry of Commerce and Industry",
        "appointment_type": "deputation",
        "extension_date": "2026-12-29",
        "original_appointment": "2021-12-29",
        "batch_year": 2021,
    },
    {
        "name": "Harsha Bhowmik",
        "position": "Director",
        "department": "Department of Economic Affairs",
        "ministry": "Ministry of Finance",
        "appointment_type": "contract",
        "extension_date": "2027-01-19",
        "original_appointment": "2022-01-19",
        "batch_year": 2021,
    },
    {
        "name": "Prabhu Narayan",
        "position": "Director",
        "department": "Department of Economic Affairs",
        "ministry": "Ministry of Finance",
        "appointment_type": "deputation",
        "extension_date": "2025-12-30",
        "original_appointment": "2021-12-30",
        "batch_year": 2021,
    },
    {
        "name": "Mateshwari Prasad Mishra",
        "position": "Director",
        "department": "Department of Food & Public Distribution",
        "ministry": "Ministry of Consumer Affairs, Food and Public Distribution",
        "appointment_type": "deputation",
        "extension_date": "2026-12-30",
        "original_appointment": "2021-12-30",
        "batch_year": 2021,
    },
    {
        "name": "Haimanti Bhattacharya",
        "position": "Director",
        "department": "Department of Legal Affairs",
        "ministry": "Ministry of Law and Justice",
        "appointment_type": "contract",
        "extension_date": "2026-01-11",
        "original_appointment": "2022-01-11",
        "batch_year": 2021,
    },
    {
        "name": "Mandakini Balodhi",
        "position": "Director",
        "department": "Department of Financial Services",
        "ministry": "Ministry of Finance",
        "appointment_type": "deputation",
        "extension_date": "2026-12-15",
        "original_appointment": "2021-12-15",
        "batch_year": 2021,
    },
    {
        "name": "Kapil Ashok Bendre",
        "position": "Director",
        "department": "Department of Agriculture, Cooperation & Farmers Welfare",
        "ministry": "Ministry of Agriculture and Farmers Welfare",
        "appointment_type": "contract",
        "extension_date": "2026-12-30",
        "original_appointment": "2021-12-30",
        "batch_year": 2021,
    },
    {
        "name": "Shekhar Chaudhary",
        "position": "Director",
        "department": "Department of Economic Affairs",
        "ministry": "Ministry of Finance",
        "appointment_type": "deputation",
        "extension_date": "2025-12-27",
        "original_appointment": "2021-12-27",
        "batch_year": 2021,
    },
    {
        "name": "Neeraj Gaba",
        "position": "Director",
        "department": "Department of Commerce",
        "ministry": "Ministry of Commerce and Industry",
        "appointment_type": "contract",
        "extension_date": "2026-02-27",
        "original_appointment": "2022-02-28",
        "batch_year": 2021,
    },
    {
        "name": "Hardik Mukesh Sheth",
        "position": "Director",
        "department": "Department of Financial Services",
        "ministry": "Ministry of Finance",
        "appointment_type": "deputation",
        "extension_date": "2027-01-03",
        "original_appointment": "2022-01-03",
        "batch_year": 2021,
    },
    {
        "name": "Bidur Kant Jha",
        "position": "Director",
        "department": "Department of Road Transport & Highways",
        "ministry": "Ministry of Road Transport and Highways",
        "appointment_type": "contract",
        "extension_date": "2026-12-14",
        "original_appointment": "2021-12-14",
        "batch_year": 2021,
    },
    {
        "name": "Gaurav Kishor Joshi",
        "position": "Deputy Secretary",
        "department": "Department of Heavy Industry",
        "ministry": "Ministry of Heavy Industries",
        "appointment_type": "contract",
        "extension_date": "2026-01-09",
        "original_appointment": "2022-01-10",
        "batch_year": 2021,
    },
    {
        "name": "G. Sarathy Raja",
        "position": "Deputy Secretary",
        "department": "Department of Steel",
        "ministry": "Ministry of Steel",
        "appointment_type": "contract",
        "extension_date": "2027-02-06",
        "original_appointment": "2022-02-06",
        "batch_year": 2021,
    },
]


def update_database():
    """Update database with verified information"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Add new columns if they don't exist
        print("Adding new columns to lateral_entrants table...")
        try:
            cursor.execute(
                "ALTER TABLE lateral_entrants ADD COLUMN appointment_type VARCHAR(50)"
            )
            print("  ✓ Added appointment_type column")
        except sqlite3.OperationalError:
            print("  - appointment_type column already exists")

        try:
            cursor.execute(
                "ALTER TABLE lateral_entrants ADD COLUMN extension_date DATE"
            )
            print("  ✓ Added extension_date column")
        except sqlite3.OperationalError:
            print("  - extension_date column already exists")

        try:
            cursor.execute(
                "ALTER TABLE lateral_entrants ADD COLUMN current_status VARCHAR(100)"
            )
            print("  ✓ Added current_status column")
        except sqlite3.OperationalError:
            print("  - current_status column already exists")

        try:
            cursor.execute(
                "ALTER TABLE lateral_entrants ADD COLUMN verified_source TEXT"
            )
            print("  ✓ Added verified_source column")
        except sqlite3.OperationalError:
            print("  - verified_source column already exists")

        conn.commit()

        # Update each verified officer
        print("\n" + "=" * 80)
        print("UPDATING VERIFIED OFFICERS")
        print("=" * 80 + "\n")

        source = "The Secretariat article (Dec 19, 2024): https://thesecretariat.in/article/govt-extends-term-for-17-laterally-recruited-officers"

        for officer in VERIFIED_OFFICERS:
            print(f"Processing: {officer['name']}")

            # Try to find existing record
            cursor.execute(
                """
                SELECT id, department FROM lateral_entrants 
                WHERE name = ? 
                ORDER BY id DESC LIMIT 1
            """,
                (officer["name"],),
            )

            existing = cursor.fetchone()

            if existing:
                record_id, old_dept = existing
                print(f"  ✓ Found existing record (ID: {record_id})")

                # Update the record
                cursor.execute(
                    """
                    UPDATE lateral_entrants 
                    SET position = ?,
                        department = ?,
                        ministry = ?,
                        appointment_type = ?,
                        extension_date = ?,
                        date_of_appointment = ?,
                        current_status = ?,
                        verified_source = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """,
                    (
                        officer["position"],
                        officer["department"],
                        officer["ministry"],
                        officer["appointment_type"],
                        officer["extension_date"],
                        officer["original_appointment"],
                        "Active - Extended Term",
                        source,
                        record_id,
                    ),
                )

                print(f"  ✓ Updated: {old_dept} → {officer['department']}")
                print(f"  ✓ Status: Active (Extended to {officer['extension_date']})")
                print(f"  ✓ Type: {officer['appointment_type']}")

            else:
                # Insert new record (only Govind K Bansal should be new)
                print(f"  ! NEW OFFICER - Not found in database")

                cursor.execute(
                    """
                    INSERT INTO lateral_entrants (
                        name, batch_year, position, department, ministry,
                        date_of_appointment, extension_date, appointment_type,
                        current_status, verified_source
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        officer["name"],
                        officer["batch_year"],
                        officer["position"],
                        officer["department"],
                        officer["ministry"],
                        officer["original_appointment"],
                        officer["extension_date"],
                        officer["appointment_type"],
                        "Active - Extended Term",
                        source,
                    ),
                )

                print(
                    f"  ✓ Added new officer: {officer['position']}, {officer['department']}"
                )
                print(f"  ✓ Extension date: {officer['extension_date']}")

            print()

        conn.commit()

        # Show summary statistics
        print("=" * 80)
        print("UPDATE SUMMARY")
        print("=" * 80 + "\n")

        cursor.execute("""
            SELECT COUNT(*) FROM lateral_entrants 
            WHERE current_status = 'Active - Extended Term'
        """)
        active_count = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM lateral_entrants WHERE appointment_type = 'contract'"
        )
        contract_count = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM lateral_entrants WHERE appointment_type = 'deputation'"
        )
        deputation_count = cursor.fetchone()[0]

        cursor.execute(
            "SELECT batch_year, COUNT(*) FROM lateral_entrants GROUP BY batch_year ORDER BY batch_year"
        )
        batch_stats = cursor.fetchall()

        print(f"✓ Officers with extended terms: {active_count}")
        print(f"✓ Contract appointments: {contract_count}")
        print(f"✓ Deputation appointments: {deputation_count}")
        print(f"\nBatch Statistics:")
        for year, count in batch_stats:
            print(f"  {year}: {count} officers")

        print("\n" + "=" * 80)
        print("DATABASE UPDATE COMPLETE")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    print("=" * 80)
    print("LATERAL ENTRY DATABASE UPDATE")
    print("Verified Information from The Secretariat (Dec 19, 2024)")
    print("=" * 80 + "\n")

    update_database()

    print("\n✓ Run './export_static_data.sh' to update JSON files for deployment")
