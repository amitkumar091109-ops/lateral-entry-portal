#!/usr/bin/env python3
"""
Script to research and update lateral entry profiles with detailed information
from web sources including education, background, LinkedIn, and photos.
"""

import sqlite3
import json
import os
from datetime import datetime


class ProfileResearcher:
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

        # Create photos directory if it doesn't exist
        os.makedirs(self.photos_dir, exist_ok=True)

        # Load existing citations or create new
        if os.path.exists(self.citations_file):
            with open(self.citations_file, "r") as f:
                self.citations = json.load(f)
        else:
            self.citations = {}

    def get_all_entrants(self):
        """Get all lateral entrants from database"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, position, department, batch_year, 
                   photo_url, educational_background, previous_experience,
                   profile_summary
            FROM lateral_entrants 
            ORDER BY batch_year, name
        """)

        entrants = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return entrants

    def update_entrant_profile(self, entrant_id, updates):
        """Update entrant profile in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Update main profile
        if "profile" in updates:
            profile = updates["profile"]
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
                    profile.get("summary"),
                    profile.get("education"),
                    profile.get("experience"),
                    profile.get("photo_url"),
                    profile.get("sources"),
                    entrant_id,
                ),
            )

        # Update education details
        if "education" in updates:
            for edu in updates["education"]:
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO education_details 
                    (entrant_id, degree_type, degree_name, institution, 
                     specialization, year_of_completion)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        entrant_id,
                        edu.get("degree_type"),
                        edu.get("degree_name"),
                        edu.get("institution"),
                        edu.get("specialization"),
                        edu.get("year"),
                    ),
                )

        # Update professional details
        if "professional" in updates:
            prof = updates["professional"]
            cursor.execute(
                """
                INSERT OR REPLACE INTO professional_details
                (entrant_id, previous_company, previous_position, 
                 industry_sector, years_experience, domain_expertise)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    entrant_id,
                    prof.get("company"),
                    prof.get("position"),
                    prof.get("industry"),
                    prof.get("years_experience"),
                    prof.get("expertise"),
                ),
            )

        # Update social media profiles
        if "social" in updates:
            for platform, url in updates["social"].items():
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO social_media_profiles
                    (entrant_id, platform, profile_url)
                    VALUES (?, ?, ?)
                """,
                    (entrant_id, platform, url),
                )

        conn.commit()
        conn.close()

    def save_citations(self):
        """Save citations to JSON file"""
        with open(self.citations_file, "w") as f:
            json.dump(self.citations, indent=2, fp=f)

    def add_citation(self, entrant_id, name, citation):
        """Add citation for an entrant"""
        if str(entrant_id) not in self.citations:
            self.citations[str(entrant_id)] = {
                "name": name,
                "sources": [],
                "last_updated": datetime.now().isoformat(),
            }

        self.citations[str(entrant_id)]["sources"].append(citation)
        self.citations[str(entrant_id)]["last_updated"] = datetime.now().isoformat()
        self.save_citations()

    def display_research_template(self, entrant):
        """Display template for manual research"""
        print(f"\n{'=' * 80}")
        print(f"RESEARCHING: {entrant['name']}")
        print(f"{'=' * 80}")
        print(f"ID: {entrant['id']}")
        print(f"Position: {entrant['position']}")
        print(f"Department: {entrant['department']}")
        print(f"Batch Year: {entrant['batch_year']}")
        print(f"\nCurrent Data:")
        print(
            f"  Education: {entrant.get('educational_background') or 'Not available'}"
        )
        print(f"  Experience: {entrant.get('previous_experience') or 'Not available'}")
        print(f"  Photo: {entrant.get('photo_url') or 'Not available'}")
        print(f"\nSearch Queries to Use:")
        print(f'  1. "{entrant["name"]} India government"')
        print(f'  2. "{entrant["name"]} {entrant["position"]} {entrant["department"]}"')
        print(f'  3. "{entrant["name"]} LinkedIn"')
        print(f'  4. "{entrant["name"]} education background"')
        print(f"\n")


if __name__ == "__main__":
    researcher = ProfileResearcher()
    entrants = researcher.get_all_entrants()

    print(f"Total Entrants to Research: {len(entrants)}")
    print(f"\nThis script will help research each profile systematically.")
    print(f"Photos will be saved to: {researcher.photos_dir}")
    print(f"Citations will be saved to: {researcher.citations_file}")

    # Display first entrant as example
    if entrants:
        researcher.display_research_template(entrants[0])
        print("\nReady to start research. Use Perplexity to search for each profile.")
