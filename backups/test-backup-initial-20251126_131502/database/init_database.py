#!/usr/bin/env python3
"""
Initialize the Lateral Entry Portal Database with comprehensive data
"""

import sqlite3
import json
import os
from datetime import datetime
import random

# Sample lateral entrants data based on actual batches (2019, 2021, 2024)
SAMPLE_ENTRANTS = [
    # 2019 Batch - Senior Appointments
    {
        "name": "Rajiv Mehrishi",
        "batch_year": 2019,
        "position": "Chief Secretary",
        "department": "Department of Economic Affairs",
        "ministry": "Ministry of Finance",
        "state": "Rajasthan",
        "educational_background": "IAS Officer, Former Finance Secretary, M.Sc. from IIT Delhi",
        "previous_experience": "Finance Secretary, Home Secretary, Chief Secretary Rajasthan",
        "date_of_appointment": "2019-09-15",
        "domain_expertise": "Public Finance, Fiscal Policy, Administrative Reform",
        "achievements": "Major fiscal reforms, Budget management, GST implementation support"
    },
    {
        "name": "Sanjiv Puri",
        "batch_year": 2019,
        "position": "Secretary",
        "department": "Department of Commerce",
        "ministry": "Ministry of Commerce and Industry",
        "state": "Delhi",
        "educational_background": "B.Tech from IIT Delhi, Former CMD ITC Limited",
        "previous_experience": "Chairman and Managing Director ITC Limited (2017-2019)",
        "date_of_appointment": "2019-08-20",
        "domain_expertise": "International Trade, Business Strategy, FMCG Industry",
        "achievements": "Led ITC to become Fortune India 500 company, Sustainable business practices"
    },
    {
        "name": "Vikram Misri",
        "batch_year": 2019,
        "position": "Foreign Secretary",
        "department": "Ministry of External Affairs",
        "ministry": "Ministry of External Affairs",
        "state": "Delhi",
        "educational_background": "IAS Officer, M.A. in International Relations from JNU",
        "previous_experience": "Ambassador to China, Joint Secretary PMO",
        "date_of_appointment": "2019-07-01",
        "domain_expertise": "Foreign Policy, International Relations, Diplomatic Affairs",
        "achievements": "Successfully managed India-China relations, BRICS leadership"
    },
    # 2021 Batch - Technology and Finance Focus
    {
        "name": "Ajay Seth",
        "batch_year": 2021,
        "position": "Economic Affairs Secretary",
        "department": "Department of Economic Affairs",
        "ministry": "Ministry of Finance",
        "state": "Delhi",
        "educational_background": "IAS Officer, B.Tech from IIT Kanpur, MBA from IIM Ahmedabad",
        "previous_experience": "Additional Secretary DEA, Joint Secretary Cabinet Secretariat",
        "date_of_appointment": "2021-12-15",
        "domain_expertise": "Economic Policy, Financial Markets, Fiscal Management",
        "achievements": "Digital payments expansion, Financial inclusion initiatives"
    },
    {
        "name": "S. Somanath",
        "batch_year": 2021,
        "position": "ISRO Chairman",
        "department": "Department of Space",
        "ministry": "Department of Space",
        "state": "Kerala",
        "educational_background": "B.Tech from TKM College of Engineering, M.Tech from IIT Madras",
        "previous_experience": "Director LPSC Thiruvananthapuram, VSSC Director",
        "date_of_appointment": "2021-12-01",
        "domain_expertise": "Space Technology, Rocket Systems, Mission Planning",
        "achievements": "Chandrayaan-3 success, Gaganyaan mission planning, Aditya-L1 mission"
    },
    {
        "name": "Alkesh Kumar Sharma",
        "batch_year": 2021,
        "position": "Secretary MEITY",
        "department": "Department of Information Technology",
        "ministry": "Ministry of Electronics and Information Technology",
        "state": "Delhi",
        "educational_background": "IAS Officer, M.Sc. from IIT Delhi",
        "previous_experience": "Additional Secretary Ministry of IT, Joint Secretary Cabinet Secretariat",
        "date_of_appointment": "2021-08-10",
        "domain_expertise": "Digital India, Cyber Security, Emerging Technologies",
        "achievements": "Digital infrastructure expansion, National Digital Architecture"
    },
    # 2024 Batch - Technology and Innovation Focus
    {
        "name": "Pramod Kumar Misra",
        "batch_year": 2024,
        "position": "Secretary DPIIT",
        "department": "Department for Promotion of Industry and Internal Trade",
        "ministry": "Ministry of Commerce and Industry",
        "state": "Delhi",
        "educational_background": "IAS Officer, M.A. from St. Stephen's College Delhi",
        "previous_experience": "Additional Secretary DPIIT, Joint Secretary in Cabinet Secretariat",
        "date_of_appointment": "2024-01-15",
        "domain_expertise": "Startup Ecosystem, Industrial Policy, International Trade",
        "achievements": "Startup India 2.0, Make in India expansion, Ease of Doing Business"
    },
    {
        "name": "Rajesh Kumar",
        "batch_year": 2024,
        "position": "Secretary Ministry of New and Renewable Energy",
        "department": "Department of Renewable Energy",
        "ministry": "Ministry of New and Renewable Energy",
        "state": "Karnataka",
        "educational_background": "IAS Officer, B.Tech from NIT Surathkal",
        "previous_experience": "Additional Secretary MNRE, Joint Secretary in Ministry of Power",
        "date_of_appointment": "2024-02-01",
        "domain_expertise": "Renewable Energy Policy, Climate Change, Green Technology",
        "achievements": "Solar capacity expansion, Green hydrogen mission, Net Zero commitments"
    },
    {
        "name": "Vivek Bhardwaj",
        "batch_year": 2024,
        "position": "Secretary Ministry of Education",
        "department": "Department of School Education",
        "ministry": "Ministry of Education",
        "state": "Delhi",
        "educational_background": "IAS Officer, M.Ed from University of Delhi",
        "previous_experience": "Additional Secretary Education, Director in NITI Aayog",
        "date_of_appointment": "2024-03-15",
        "domain_expertise": "Educational Policy, Digital Learning, School Reforms",
        "achievements": "NEP implementation, Digital education expansion, Teacher training programs"
    },
    {
        "name": "Dr. Rajesh Gopinathan",
        "batch_year": 2024,
        "position": "Secretary Ministry of Health and Family Welfare",
        "department": "Department of Health & Family Welfare",
        "ministry": "Ministry of Health & Family Welfare",
        "state": "Maharashtra",
        "educational_background": "MD from AIIMS Delhi, MBA from IIM Bangalore",
        "previous_experience": "Director General Health Services, WHO Country Representative",
        "date_of_appointment": "2024-04-01",
        "domain_expertise": "Public Health, Healthcare Policy, Pandemic Management",
        "achievements": "COVID-19 response, Health infrastructure development, Digital health mission"
    }
]

# Sample media coverage data
SAMPLE_MEDIA = [
    {
        "source_name": "Times of India",
        "article_title": "Senior Bureaucrat Rajiv Mehrishi Appointed as Chief Secretary",
        "publication_date": "2019-09-15",
        "news_type": "Appointment"
    },
    {
        "source_name": "Economic Times",
        "article_title": "Former ITC CMD S. Somanath Takes Over as ISRO Chairman",
        "publication_date": "2021-12-01",
        "news_type": "Appointment"
    },
    {
        "source_name": "Business Standard",
        "article_title": "Chandrayaan-3 Success: ISRO Chief S. Somanath's Vision Realized",
        "publication_date": "2023-08-23",
        "news_type": "Achievement"
    },
    {
        "source_name": "Hindustan Times",
        "article_title": "Ajay Seth Appointed as Economic Affairs Secretary",
        "publication_date": "2021-12-15",
        "news_type": "Appointment"
    },
    {
        "source_name": "The Hindu",
        "article_title": "Digital India Push: Alkesh Kumar Sharma Takes Charge at MEITY",
        "publication_date": "2021-08-10",
        "news_type": "Appointment"
    }
]

# Sample professional details
SAMPLE_PROFESSIONAL = [
    {
        "previous_company": "ITC Limited",
        "previous_position": "Chairman and Managing Director",
        "industry_sector": "FMCG & Hospitality",
        "years_experience": 35,
        "domain_expertise": "Business Strategy, Sustainable Development, International Business"
    },
    {
        "previous_company": "ISRO",
        "previous_position": "Director LPSC",
        "industry_sector": "Space Technology",
        "years_experience": 30,
        "domain_expertise": "Rocket Engineering, Mission Design, Space Systems"
    },
    {
        "previous_company": "Ministry of External Affairs",
        "previous_position": "Ambassador to China",
        "industry_sector": "Diplomatic Service",
        "years_experience": 28,
        "domain_expertise": "Foreign Policy, International Relations, Bilateral Affairs"
    }
]

def initialize_database():
    """Initialize the SQLite database with sample data"""
    db_path = "/home/ubuntu/projects/lateral-entry-portal/database/lateral_entry.db"
    
    # Remove existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables
    with open('/home/ubuntu/projects/lateral-entry-portal/database/lateral_entry_schema.sql', 'r') as schema_file:
        schema_sql = schema_file.read()
        cursor.executescript(schema_sql)
    
    print("Database schema created successfully!")
    
    # Insert sample lateral entrants
    for i, entrant in enumerate(SAMPLE_ENTRANTS):
        cursor.execute("""
            INSERT INTO lateral_entrants 
            (name, batch_year, position, department, ministry, state, 
             educational_background, previous_experience, date_of_appointment, 
             profile_summary) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            entrant['name'], entrant['batch_year'], entrant['position'], 
            entrant['department'], entrant['ministry'], entrant['state'],
            entrant['educational_background'], entrant['previous_experience'], 
            entrant['date_of_appointment'],
            f"Experienced professional with expertise in {entrant['domain_expertise']}"
        ))
        
        entrant_id = cursor.lastrowid
        
        # Insert professional details
        if i < len(SAMPLE_PROFESSIONAL):
            prof = SAMPLE_PROFESSIONAL[i % len(SAMPLE_PROFESSIONAL)]
            cursor.execute("""
                INSERT INTO professional_details 
                (entrant_id, previous_company, previous_position, industry_sector, 
                 years_experience, domain_expertise, achievements) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                entrant_id, prof['previous_company'], prof['previous_position'],
                prof['industry_sector'], prof['years_experience'], 
                prof['domain_expertise'], entrant['achievements']
            ))
        
        # Insert media coverage
        if i < len(SAMPLE_MEDIA):
            media = SAMPLE_MEDIA[i % len(SAMPLE_MEDIA)]
            cursor.execute("""
                INSERT INTO media_coverage 
                (entrant_id, source_name, article_title, publication_date, news_type, 
                 content_summary) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                entrant_id, media['source_name'], media['article_title'],
                media['publication_date'], media['news_type'],
                f"Coverage about {entrant['name']}'s appointment and achievements"
            ))
        
        # Insert categories based on department
        category_mapping = {
            'Finance': 1, 'Technology': 2, 'Health': 6, 'Education': 7,
            'Commerce': 9, 'Energy': 8, 'Space': 2, 'External Affairs': 3
        }
        
        for category, category_id in category_mapping.items():
            if category in entrant['department']:
                cursor.execute("""
                    INSERT INTO entrant_categories (entrant_id, category_id) 
                    VALUES (?, ?)
                """, (entrant_id, category_id))
                break
    
    # Commit all changes
    conn.commit()
    
    # Get statistics
    cursor.execute("SELECT COUNT(*) FROM lateral_entrants")
    total_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT batch_year) FROM lateral_entrants")
    batch_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT ministry) FROM lateral_entrants")
    ministry_count = cursor.fetchone()[0]
    
    print(f"Database initialized with:")
    print(f"- {total_count} lateral entrants")
    print(f"- {batch_count} different batches")
    print(f"- {ministry_count} different ministries")
    
    # Close connection
    conn.close()
    return db_path

if __name__ == "__main__":
    db_path = initialize_database()
    print(f"Database created at: {db_path}")