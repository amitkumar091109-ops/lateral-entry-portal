#!/usr/bin/env python3
"""
Interactive profile updater for lateral entry appointees.
Run this script to systematically research and update each profile.
"""

import sqlite3
import json
import os
import sys
from datetime import datetime


class ProfileUpdater:
    def __init__(
        self,
        db_path="/home/ubuntu/projects/lateral-entry-portal/database/lateral_entry.db",
    ):
        self.db_path = db_path
        self.photos_dir = (
            "/home/ubuntu/projects/lateral-entry-portal/assets/images/profiles"
        )
        self.citations_file = (
            "/home/ubuntu/projects/lateral-entry-portal/research_citations.json"
        )

        os.makedirs(self.photos_dir, exist_ok=True)

        if os.path.exists(self.citations_file):
            with open(self.citations_file, "r") as f:
                self.citations = json.load(f)
        else:
            self.citations = {}

    def get_entrant(self, entrant_id):
        """Get entrant details by ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM lateral_entrants WHERE id = ?
        """,
            (entrant_id,),
        )

        entrant = dict(cursor.fetchone()) if cursor.fetchone() else None
        conn.close()
        return entrant

    def update_profile(self, entrant_id, data):
        """Update entrant profile with researched data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Update main profile
            cursor.execute(
                """
                UPDATE lateral_entrants 
                SET profile_summary = ?,
                    educational_background = ?,
                    previous_experience = ?,
                    photo_url = ?,
                    verified_source = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """,
                (
                    data.get("profile_summary", ""),
                    data.get("educational_background", ""),
                    data.get("previous_experience", ""),
                    data.get("photo_url", ""),
                    data.get("verified_source", ""),
                    entrant_id,
                ),
            )

            # Add education details
            if "education_entries" in data:
                for edu in data["education_entries"]:
                    cursor.execute(
                        """
                        INSERT INTO education_details 
                        (entrant_id, degree_type, degree_name, institution, 
                         specialization, year_of_completion)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """,
                        (
                            entrant_id,
                            edu.get("degree_type", ""),
                            edu.get("degree_name", ""),
                            edu.get("institution", ""),
                            edu.get("specialization", ""),
                            edu.get("year", None),
                        ),
                    )

            # Add professional details
            if "professional" in data:
                prof = data["professional"]
                cursor.execute(
                    """
                    INSERT INTO professional_details
                    (entrant_id, previous_company, previous_position, 
                     industry_sector, years_experience, domain_expertise, achievements)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        entrant_id,
                        prof.get("company", ""),
                        prof.get("position", ""),
                        prof.get("industry", ""),
                        prof.get("years_experience", None),
                        prof.get("expertise", ""),
                        prof.get("achievements", ""),
                    ),
                )

            # Add social media profiles
            if "social_media" in data:
                for platform, url in data["social_media"].items():
                    cursor.execute(
                        """
                        INSERT INTO social_media_profiles
                        (entrant_id, platform, profile_url, verified)
                        VALUES (?, ?, ?, ?)
                    """,
                        (entrant_id, platform, url, True),
                    )

            conn.commit()
            print(f"✓ Successfully updated profile ID {entrant_id}")
            return True

        except Exception as e:
            conn.rollback()
            print(f"✗ Error updating profile: {e}")
            return False
        finally:
            conn.close()

    def save_citation(self, entrant_id, name, citations_data):
        """Save research citations"""
        self.citations[str(entrant_id)] = {
            "name": name,
            "citations": citations_data,
            "last_updated": datetime.now().isoformat(),
        }

        with open(self.citations_file, "w") as f:
            json.dump(self.citations, indent=2, fp=f)
        print(f"✓ Saved citations for {name}")


def example_update_amber_dubey():
    """Example update for Amber Dubey based on available information"""
    updater = ProfileUpdater()

    # Example data structure - fill this in after research
    data = {
        "profile_summary": "Experienced aviation professional appointed as Joint Secretary in Ministry of Civil Aviation in 2019 through lateral entry scheme.",
        "educational_background": "Engineering graduate with MBA from premier institutions.",
        "previous_experience": "Over 15 years of experience in aviation sector and technology management.",
        "photo_url": "/assets/images/profiles/11_amber_dubey.jpg",
        "verified_source": json.dumps(
            [
                {
                    "type": "official",
                    "title": "PIB Press Release - Lateral Entry",
                    "url": "https://pib.gov.in/PressReleasePage.aspx?PRID=1574879",
                    "date": "2019-06-15",
                }
            ]
        ),
        "education_entries": [
            {
                "degree_type": "Bachelor",
                "degree_name": "B.Tech",
                "institution": "Indian Institute of Technology",
                "specialization": "Computer Science",
                "year": 2005,
            },
            {
                "degree_type": "Master",
                "degree_name": "MBA",
                "institution": "Indian Institute of Management",
                "specialization": "Business Administration",
                "year": 2008,
            },
        ],
        "professional": {
            "company": "Aviation Technology Firm",
            "position": "Senior Executive",
            "industry": "Aviation & Technology",
            "years_experience": 15,
            "expertise": "Aviation policy, technology management, operations",
            "achievements": "Led major aviation technology initiatives",
        },
        "social_media": {"linkedin": "https://linkedin.com/in/amberdubey"},
    }

    # Uncomment to actually update:
    # updater.update_profile(11, data)
    # updater.save_citation(11, 'Amber Dubey', data['verified_source'])

    print("Example data structure prepared.")
    print(
        "After completing web research, update the data dictionary and uncomment the update calls."
    )


if __name__ == "__main__":
    print("Lateral Entry Profile Updater")
    print("=" * 80)
    print("\nThis script helps you systematically update profiles after research.")
    print("\nSteps:")
    print("1. Research a profile using Google, LinkedIn, news sources")
    print("2. Collect information: education, experience, photo, citations")
    print("3. Update the data dictionary in this script")
    print("4. Run the update function")
    print("\nExample function provided: example_update_amber_dubey()")
    print("\nTo update a profile, modify the example function with your research.")
    print("=" * 80)

    # Show example
    example_update_amber_dubey()
