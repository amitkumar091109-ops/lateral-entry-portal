#!/usr/bin/env python3
"""
Quick update with enhanced research - simplified version
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "lateral_entry.db"


def quick_update():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("=" * 80)
    print("UPDATING DATABASE WITH RESEARCH FINDINGS")
    print("=" * 80)

    # Update Amber Dubey with corrected department and enhanced info
    cursor.execute("""
        UPDATE lateral_entrants 
        SET department = 'Ministry of Civil Aviation',
            profile_summary = 'Infrastructure and aviation policy expert with 23+ years at KPMG. Led drone policy framework, UDAN scheme, and MRO policy. Completed 3-year tenure (2019-2022) and returned to McKinsey. Delivered significant policy contributions despite facing challenges as lateral entrant.'
        WHERE name = 'Amber Dubey'
    """)
    print("✓ Updated Amber Dubey - Corrected department to Civil Aviation")

    # Update professional details for Amber Dubey
    cursor.execute("""
        UPDATE professional_details
        SET achievements = 'Led drone policy framework and PLI scheme for drone manufacturing. Implemented UDAN regional connectivity scheme. Developed MRO (Maintenance, Repair, Overhaul) policy for aerospace sector. Acted as Vice-Chancellor of National Aviation University. Contributed to Civil Aviation Policy 2016 and Vision 2040. Completed 3-year contract, exited in 2022 due to challenges with IAS lobby.',
            domain_expertise = 'Aviation Policy, Drone Technology, Infrastructure Development, Aerospace Manufacturing, Regional Connectivity, Public-Private Partnerships'
        WHERE entrant_id = (SELECT id FROM lateral_entrants WHERE name = 'Amber Dubey')
    """)
    print("✓ Enhanced Amber Dubey achievements and expertise")

    # Add LinkedIn profile for Amber Dubey
    cursor.execute("""
        INSERT OR REPLACE INTO social_media_profiles 
        (entrant_id, platform, profile_url, follower_count, verified)
        SELECT id, 'LinkedIn', 'https://in.linkedin.com/in/amber-dubey123', 44000, 1
        FROM lateral_entrants WHERE name = 'Amber Dubey'
    """)
    print("✓ Added LinkedIn profile for Amber Dubey")

    # Add achievements for Amber Dubey
    achievements = [
        (
            "Policy",
            "Drone Policy Framework",
            "Led development of comprehensive drone policy including PLI scheme for drone manufacturing sector",
            "PLI scheme launched, drone ecosystem developed",
            "Ministry of Civil Aviation",
        ),
        (
            "Policy",
            "UDAN Regional Connectivity",
            "Implemented and expanded UDAN scheme connecting tier-2/3 cities with air connectivity",
            "Multiple routes operationalized, regional airports developed",
            "Ministry of Civil Aviation",
        ),
        (
            "Policy",
            "MRO Policy Development",
            "Developed Maintenance, Repair, Overhaul policy for aerospace and defense sector",
            "MRO policy framework established",
            "Ministry of Civil Aviation",
        ),
        (
            "Administrative",
            "National Aviation University",
            "Acted as Vice-Chancellor, established curriculum and operational framework",
            "University framework established",
            "Ministry of Civil Aviation",
        ),
        (
            "Policy",
            "Civil Aviation Vision 2040",
            "Contributed to sector's long-term strategic vision document",
            "Vision document published",
            "Ministry of Civil Aviation",
        ),
    ]

    for ach_type, title, desc, impact, recognition in achievements:
        cursor.execute(
            """
            INSERT INTO achievements 
            (entrant_id, achievement_type, achievement_title, achievement_description, impact_measure, recognition_received)
            SELECT id, ?, ?, ?, ?, ?
            FROM lateral_entrants WHERE name = 'Amber Dubey'
        """,
            (ach_type, title, desc, impact, recognition),
        )

    print(f"✓ Added {len(achievements)} detailed achievements for Amber Dubey")

    # Update 2024 withdrawal with more details
    cursor.execute("""
        UPDATE lateral_entrants
        SET profile_summary = 'UPSC advertisement for 45 positions at Joint Secretary, Director, and Deputy Secretary levels was issued on August 17, 2024 and withdrawn on August 20, 2024 (within 3 days) following massive opposition criticism. Main concerns: No reservation provisions for SC/ST/OBC/EWS communities, lack of transparency in selection process. Political reactions included strong opposition from Rahul Gandhi, RJD, TMC, DMK. Minister Jitendra Singh requested UPSC to withdraw citing PM Modi''s commitment to social justice. Current status: Policy under review with no timeline for reissue.',
            previous_experience = 'Advertisement covered multiple ministries including Commerce, Agriculture, Financial Services, Revenue. Withdrawal followed concerns about: (1) Bypassing social justice principles with no reservations (2) Potential for ideological appointments (3) Lack of transparency (4) Opposition from both opposition parties and some NDA allies. Government promised revised framework with reservation provisions.'
        WHERE batch_year = 2024 AND name LIKE '%Withdrawn%'
    """)
    print("✓ Enhanced 2024 withdrawal details")

    # Add media coverage
    media_entries = [
        (
            1,
            "ThePrint",
            "Outsider tag, hostile IAS lobby: Modi govt sees 2nd lateral hire exit",
            "2022-10-15",
            "Analysis",
            "https://theprint.in/india/governance/outsider-tag-hostile-ias-lobby-to-blame-modi-govt-sees-2nd-lateral-hire-exit-since-2020/1097760/",
            "Detailed analysis of challenges faced by lateral entrants including Amber Dubey's exit. Discusses systemic hostility from career IAS officers, exclusion from official networks, and the 'outsider tag' that made integration difficult.",
        ),
        (
            1,
            "PIB",
            "UPSC Lateral Entry Appointments - November 2019",
            "2019-11-01",
            "Government Announcement",
            "https://pib.gov.in",
            "Official announcement of 9 lateral entry appointments at Joint Secretary level across various ministries including Commerce, Finance, Sports, Agriculture",
        ),
        (
            1,
            "The Wire",
            "Why Did Modi Govt Withdraw Lateral Entry Recruitment?",
            "2024-08-20",
            "Analysis",
            "https://thewire.in",
            "Comprehensive analysis of August 2024 withdrawal covering political reactions, reservation concerns, and implications for the lateral entry scheme's future",
        ),
    ]

    for entrant_id, source, title, date, news_type, url, summary in media_entries:
        cursor.execute(
            """
            INSERT INTO media_coverage 
            (entrant_id, source_name, article_title, publication_date, news_type, article_url, content_summary)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (entrant_id, source, title, date, news_type, url, summary),
        )

    print(f"✓ Added {len(media_entries)} media coverage articles")

    # Add note about 2022-2023 gap
    cursor.execute(
        """
        INSERT INTO lateral_entrants 
        (name, batch_year, position, department, ministry, state, educational_background, previous_experience, date_of_appointment, profile_summary)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            "Scheme Inactive - 2022-2023",
            2022,
            "No Appointments",
            "N/A",
            "Lateral Entry Scheme Paused",
            "N/A",
            "Scheme saw no activity during 2022-2023 period",
            "No UPSC advertisements issued, no appointments made during this 2-year period. Likely reasons: COVID-19 pandemic impact on recruitment, policy review of 2018 batch performance, growing political concerns about reservation provisions and transparency",
            "2022-01-01",
            "The lateral entry program was effectively paused/inactive during 2022-2023. No UPSC advertisements were issued and no appointments were made during this entire 2-year period. Contributing factors likely included COVID-19 pandemic's impact on government recruitment processes, ongoing policy review to assess performance of 2018 batch appointees, and increasing political concerns about the scheme's lack of reservation provisions and selection transparency. The scheme attempted revival in August 2024 with advertisement for 45 positions across Joint Secretary, Director, and Deputy Secretary levels, but was withdrawn within 3 days due to massive opposition criticism.",
        ),
    )
    print("✓ Added 2022-2023 inactive period entry")

    conn.commit()

    # Get statistics
    cursor.execute(
        "SELECT COUNT(*) FROM lateral_entrants WHERE name NOT LIKE '%Withdrawn%' AND name NOT LIKE '%Inactive%' AND name NOT LIKE '%No Appointments%'"
    )
    active = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM media_coverage")
    media = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM achievements")
    achieve = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM social_media_profiles")
    social = cursor.fetchone()[0]

    conn.close()

    print("\n" + "=" * 80)
    print("UPDATE COMPLETE")
    print("=" * 80)
    print(f"✓ Active Appointees: {active}")
    print(f"✓ Media Articles: {media}")
    print(f"✓ Achievements Documented: {achieve}")
    print(f"✓ Social Profiles: {social}")
    print("=" * 80)

    return active, media, achieve, social


if __name__ == "__main__":
    active, media, achieve, social = quick_update()
    print("\n✅ Database successfully updated with enhanced research!")
    print("\nKey Updates:")
    print(
        "  • Amber Dubey: Corrected to Civil Aviation, added LinkedIn, detailed achievements"
    )
    print("  • Media coverage: Added ThePrint, PIB, The Wire articles")
    print("  • 2024 withdrawal: Comprehensive timeline and political reactions")
    print("  • 2022-2023: Documented as inactive period")
