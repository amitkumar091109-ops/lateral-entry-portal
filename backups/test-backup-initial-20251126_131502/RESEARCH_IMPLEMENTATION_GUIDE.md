# Profile Research Implementation Guide

## Summary

Due to API limitations, the profile research needs to be done manually using web search engines. This document provides the complete framework, scripts, and workflow to systematically research and update all 65 lateral entry appointee profiles.

## Created Files

1. **research_profiles.py** - Core Python class for database operations
2. **update_profile.py** - Interactive script with example update function
3. **research_tracker.json** - Progress tracking (15 high-priority Joint Secretaries listed)
4. **PROFILE_RESEARCH_WORKFLOW.md** - Detailed research methodology
5. **research_citations.json** - Will store all source citations

## Directory Structure

```
/home/ubuntu/projects/lateral-entry-portal/
├── database/
│   └── lateral_entry.db (65 profiles to update)
├── assets/
│   └── images/
│       └── profiles/ (created - save photos here)
├── research_profiles.py (helper classes)
├── update_profile.py (update script with examples)
├── research_tracker.json (progress tracking)
├── research_citations.json (will be created after first update)
└── PROFILE_RESEARCH_WORKFLOW.md (methodology)
```

## Quick Start

### Step 1: Research a Profile Manually

For each appointee (starting with Joint Secretaries):

**Google Searches:**
```
"Amber Dubey" lateral entry India government
"Amber Dubey" Joint Secretary Civil Aviation
"Amber Dubey" LinkedIn India
"Amber Dubey" IIT IIM education
"Amber Dubey" professional background
```

**Sources to Check:**
- LinkedIn profiles
- Government press releases (pib.gov.in)
- News articles (Economic Times, Hindu, Indian Express)
- Ministry websites
- Company/organization websites
- Conference presentations
- Academic publications (Google Scholar)

### Step 2: Collect Information

**Required Data:**
1. **Education**
   - Degrees (B.Tech, MBA, etc.)
   - Institutions (IIT Delhi, IIM Ahmedabad, etc.)
   - Specializations
   - Years of completion

2. **Professional Experience**
   - Previous companies/organizations
   - Positions held
   - Industry sectors
   - Years of experience
   - Domain expertise
   - Major achievements

3. **Social Media**
   - LinkedIn profile URL
   - Twitter handle (if public figure)

4. **Photo**
   - Download professional photo from LinkedIn or official sources
   - Save as: `[id]_[name_slug].jpg`
   - Place in: `/home/ubuntu/projects/lateral-entry-portal/assets/images/profiles/`

5. **Citations**
   - URL of each source
   - Title of page/article
   - Date published (if available)
   - Date accessed

### Step 3: Update Database

Edit `update_profile.py` and create a new function (copy the example):

```python
def update_amber_dubey():
    updater = ProfileUpdater()
    
    data = {
        'profile_summary': 'Brief 2-3 sentence summary of the person',
        'educational_background': 'B.Tech from IIT Delhi, MBA from IIM Ahmedabad',
        'previous_experience': 'Over 15 years in aviation sector...',
        'photo_url': '/assets/images/profiles/11_amber_dubey.jpg',
        'verified_source': json.dumps([
            {
                'type': 'official',
                'title': 'PIB Press Release',
                'url': 'https://pib.gov.in/...',
                'date': '2019-06-15',
                'accessed': '2025-11-25'
            },
            {
                'type': 'linkedin',
                'title': 'LinkedIn Profile',
                'url': 'https://linkedin.com/in/...',
                'accessed': '2025-11-25'
            }
        ]),
        'education_entries': [
            {
                'degree_type': 'Bachelor',
                'degree_name': 'B.Tech',
                'institution': 'IIT Delhi',
                'specialization': 'Computer Science',
                'year': 2005
            },
            {
                'degree_type': 'Master',
                'degree_name': 'MBA',
                'institution': 'IIM Ahmedabad',
                'specialization': 'Business Administration',
                'year': 2008
            }
        ],
        'professional': {
            'company': 'Previous Company Name',
            'position': 'Senior Vice President',
            'industry': 'Aviation & Technology',
            'years_experience': 15,
            'expertise': 'Aviation policy, operations, technology',
            'achievements': 'Led major projects, awards, etc.'
        },
        'social_media': {
            'linkedin': 'https://linkedin.com/in/amberdubey',
            'twitter': 'https://twitter.com/amberdubey'  # if available
        }
    }
    
    updater.update_profile(11, data)  # 11 is Amber Dubey's ID
    updater.save_citation(11, 'Amber Dubey', json.loads(data['verified_source']))
    print("✓ Updated Amber Dubey profile")

# Run the function
update_amber_dubey()
```

### Step 4: Run the Update

```bash
cd /home/ubuntu/projects/lateral-entry-portal
uv run python update_profile.py
```

### Step 5: Update Progress Tracker

Mark the profile as completed in `research_tracker.json`:

```json
{
  "id": 11,
  "name": "Amber Dubey",
  "researched": true,
  "photo": true,
  "education": true,
  "experience": true,
  "linkedin": true,
  "updated": true
}
```

### Step 6: Repeat for Next Profile

Continue with the next person in the priority list.

## Priority Order (15 Joint Secretaries - Start Here)

### 2019 Batch (9):
1. ✗ Amber Dubey - Civil Aviation (ID: 11)
2. ✗ Arun Goel - Commerce (ID: 12)
3. ✗ Bhushan Kumar - Ports Shipping (ID: 19)
4. ✗ Dinesh Dayanand Jagdale - Renewable Energy (ID: 17)
5. ✗ Kakoli Ghosh - Agriculture (ID: 13)
6. ✗ Rajeev Saksena - Economic Affairs (ID: 14)
7. ✗ Saurabh Mishra - Financial Services (ID: 16)
8. ✗ Sujit Kumar Bajpayee - Environment (ID: 15)
9. ✗ Suman Prasad Singh - Road Transport (ID: 18)

### 2021 Batch (3):
10. ✗ Balasubramanian Krishnamurthy - Revenue (ID: 52)
11. ✗ Manish Chadha - Commerce (ID: 51)
12. ✗ Samuel Praveen Kumar - Agriculture (ID: 20)

### 2023 Batch (3):
13. ✗ Ajay Kumar Arora - Legal Affairs (ID: 64)
14. ✗ Madhu Sudana Sankar - Civil Aviation (ID: 72)
15. ✗ Manoj Muttathil - Financial Services (ID: 75)

## Database Schema Reference

### Main Fields (lateral_entrants table):
- `profile_summary` TEXT - 2-3 sentence bio
- `educational_background` TEXT - Summary of education
- `previous_experience` TEXT - Career summary
- `photo_url` TEXT - Path to photo file
- `verified_source` TEXT - JSON array of citations

### Education Details (education_details table):
- `degree_type` - Bachelor, Master, Doctorate
- `degree_name` - B.Tech, MBA, PhD, etc.
- `institution` - University/college name
- `specialization` - Field of study
- `year_of_completion` - Year graduated

### Professional Details (professional_details table):
- `previous_company` - Company/org name
- `previous_position` - Job title
- `industry_sector` - Industry category
- `years_experience` - Total years
- `domain_expertise` - Areas of expertise
- `achievements` - Major accomplishments

### Social Media (social_media_profiles table):
- `platform` - linkedin, twitter, etc.
- `profile_url` - Full URL
- `verified` - Boolean

## Photo Guidelines

**Naming Convention:**
```
[id]_[name_in_lowercase_with_underscores].jpg
```

**Examples:**
- `11_amber_dubey.jpg`
- `12_arun_goel.jpg`
- `13_kakoli_ghosh.jpg`

**Requirements:**
- Professional headshot
- Minimum 400x400px
- JPG or PNG format
- Less than 500KB file size

**Sources (in priority order):**
1. LinkedIn public profile photos
2. Official government websites
3. Organization/company websites
4. Conference photos (with attribution)
5. News articles (fair use)

**Always save the source URL in citations!**

## Citation Format

```json
[
  {
    "type": "official",
    "title": "PIB Press Release - Lateral Entry Appointments 2019",
    "url": "https://pib.gov.in/PressReleasePage.aspx?PRID=1574879",
    "date": "2019-06-15",
    "accessed": "2025-11-25"
  },
  {
    "type": "linkedin",
    "title": "LinkedIn Profile - Amber Dubey",
    "url": "https://linkedin.com/in/amberdubey",
    "accessed": "2025-11-25"
  },
  {
    "type": "news",
    "title": "Economic Times - Nine Join Govt Through Lateral Entry",
    "url": "https://economictimes.indiatimes.com/...",
    "date": "2019-06-16",
    "accessed": "2025-11-25"
  },
  {
    "type": "photo",
    "title": "LinkedIn Profile Photo",
    "url": "https://media.licdn.com/...",
    "accessed": "2025-11-25",
    "note": "Used under fair use for government transparency portal"
  }
]
```

## After Completing All Updates

### Export to Static JSON:
```bash
cd /home/ubuntu/projects/lateral-entry-portal
./export_static_data.sh
```

This will update:
- `data/entrants.json` - All profile data
- `data/stats.json` - Statistics

### Deploy to Production:
```bash
# Copy updated files to production
sudo cp data/entrants.json /var/www/html/lateral-entry/data/
sudo cp data/stats.json /var/www/html/lateral-entry/data/
sudo cp -r assets/images/profiles/* /var/www/html/lateral-entry/assets/images/profiles/
```

## Helpful Search Tips

### Finding LinkedIn Profiles:
```
site:linkedin.com/in "[Name]" India government
site:linkedin.com/in "[Name]" IAS IPS civil service
```

### Finding Education Info:
```
"[Name]" IIT alumnus
"[Name]" IIM graduate
"[Name]" education background degree
```

### Finding Professional Experience:
```
"[Name]" worked at company
"[Name]" previous role position
"[Name]" career background experience
```

### Finding Official Announcements:
```
site:pib.gov.in "[Name]" lateral entry
site:dopt.gov.in "[Name]" appointment
"[Name]" "[Department]" joint secretary director
```

## Common Patterns Found

Many lateral entry appointees have:
- IIT degrees (B.Tech)
- IIM degrees (MBA)
- Prior work in consulting (McKinsey, BCG, Deloitte)
- Private sector experience (15-20 years)
- Domain expertise matching their department
- LinkedIn profiles (public or semi-public)

## Notes

- **Privacy**: Only use publicly available information
- **Accuracy**: Verify from multiple sources when possible
- **Attribution**: Always cite sources properly
- **Updates**: Mark `updated_at` timestamp is automatic
- **Photos**: Respect copyright - use only publicly available images with attribution

## Estimated Time

- **Per Profile**: 15-30 minutes (depending on information availability)
- **Joint Secretaries (15)**: 4-8 hours
- **Directors (42)**: 10-20 hours  
- **Deputy Secretaries (8)**: 2-4 hours
- **Total**: 16-32 hours for all 65 profiles

## Progress Tracking

Update `research_tracker.json` after each profile:
```json
{
  "research_tracker": {
    "total_profiles": 65,
    "completed": 1,
    "in_progress": 0,
    "pending": 64,
    "last_updated": "2025-11-25T15:00:00Z"
  }
}
```

## Getting Help

If you encounter issues:
1. Check database schema: `sqlite3 database/lateral_entry.db ".schema"`
2. Test update script: `uv run python update_profile.py`
3. View current data: `sqlite3 database/lateral_entry.db "SELECT * FROM lateral_entrants WHERE id=11"`
4. Check citations file: `cat research_citations.json`

## Next Steps

1. **Start with Profile ID 11 (Amber Dubey)**
2. **Research using Google, LinkedIn, news sources**
3. **Collect information systematically**
4. **Update `update_profile.py` with the data**
5. **Run the script to update database**
6. **Mark as complete in tracker**
7. **Move to next profile (ID 12 - Arun Goel)**

Good luck with the research! This systematic approach will build a comprehensive database of all lateral entry appointees.
