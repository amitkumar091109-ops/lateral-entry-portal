# Profile Research Workflow

## Overview
This document outlines the systematic process to research and update all 65 lateral entry appointee profiles with comprehensive information.

## Database Structure

### Main Tables:
- **lateral_entrants**: Core profile information
- **education_details**: Academic qualifications
- **professional_details**: Work experience
- **social_media_profiles**: LinkedIn, Twitter, etc.

### Fields to Update:
1. `photo_url` - Profile photo URL
2. `profile_summary` - Brief bio (2-3 sentences)
3. `educational_background` - Education summary
4. `previous_experience` - Career summary
5. `verified_source` - Citation URLs (JSON)

## Research Process (Per Profile)

### Step 1: Google Search
Search queries:
```
"[Name]" lateral entry India government
"[Name]" Joint Secretary [Department]
"[Name]" IIT IIM education
"[Name]" LinkedIn profile
```

### Step 2: LinkedIn Research
- Find LinkedIn profile
- Note: Education, Current/Previous positions, Skills, Endorsements
- Screenshot or save profile URL

### Step 3: News Articles
- Press releases from government websites
- PIB (Press Information Bureau) announcements
- News coverage of appointments

### Step 4: Professional Background
- Previous company websites
- Industry publications
- Conference presentations
- Academic papers (Google Scholar)

### Step 5: Photo Collection
- LinkedIn profile photo
- Official government photos
- Conference/event photos
- Save as: `[entrant_id]_[name_slug].jpg`

### Step 6: Data Entry
Use the Python script to update database:
```python
updates = {
    'profile': {
        'summary': '...',
        'education': '...',
        'experience': '...',
        'photo_url': '/assets/images/profiles/11_amber_dubey.jpg',
        'sources': json.dumps([
            {'url': '...', 'title': '...', 'accessed': '2025-11-25'},
            ...
        ])
    },
    'education': [
        {
            'degree_type': 'Bachelor',
            'degree_name': 'B.Tech',
            'institution': 'IIT Delhi',
            'specialization': 'Computer Science',
            'year': 2005
        },
        ...
    ],
    'professional': {
        'company': 'Previous Company',
        'position': 'Senior Manager',
        'industry': 'Technology',
        'years_experience': 15,
        'expertise': 'Aviation, Technology, Policy'
    },
    'social': {
        'linkedin': 'https://linkedin.com/in/...',
        'twitter': 'https://twitter.com/...'
    }
}
```

## Priority Order

### Batch 2019 (9 profiles) - Joint Secretaries
1. Amber Dubey - Civil Aviation
2. Arun Goel - Commerce
3. Bhushan Kumar - Ports Shipping
4. Dinesh Dayanand Jagdale - Renewable Energy
5. Kakoli Ghosh - Agriculture
6. Rajeev Saksena - Economic Affairs
7. Saurabh Mishra - Financial Services
8. Sujit Kumar Bajpayee - Environment
9. Suman Prasad Singh - Road Transport

### Batch 2021 (42 profiles) - Mix of positions
Research Directors first, then Deputy Secretaries

### Batch 2023 (14 profiles)
Most recent appointments

## Citation Format

```json
{
  "entrant_id": "11",
  "name": "Amber Dubey",
  "sources": [
    {
      "type": "official",
      "title": "PIB Press Release - Lateral Entry Appointments",
      "url": "https://pib.gov.in/...",
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
      "title": "Economic Times - Nine Lateral Entry Appointments",
      "url": "https://economictimes.indiatimes.com/...",
      "date": "2019-06-16",
      "accessed": "2025-11-25"
    }
  ],
  "education": [
    {
      "degree": "B.Tech Computer Science, IIT Delhi (2005)",
      "source": "LinkedIn Profile"
    },
    {
      "degree": "MBA, IIM Ahmedabad (2008)",
      "source": "LinkedIn Profile"
    }
  ],
  "professional_experience": "15 years in aviation technology and policy. Previously worked at...",
  "photo_source": "LinkedIn public profile photo",
  "last_updated": "2025-11-25T14:30:00Z"
}
```

## Tools and Resources

### Search Engines:
- Google: General search
- LinkedIn: Professional profiles
- Google Scholar: Academic publications
- PIB India: Official press releases

### Government Websites:
- https://pib.gov.in - Press Information Bureau
- https://dopt.gov.in - Department of Personnel & Training
- Individual ministry websites

### News Sources:
- The Hindu
- Economic Times
- Indian Express
- Business Standard

## Photo Guidelines

### Requirements:
- Professional headshot preferred
- Minimum resolution: 400x400px
- Format: JPG or PNG
- File naming: `[entrant_id]_[name_slug].jpg`
- Save to: `/assets/images/profiles/`

### Sources:
1. LinkedIn profile photos (public profiles)
2. Official government websites
3. Conference/event photos (with attribution)
4. News article photos (with permission/fair use)

### Attribution:
Always maintain source URL in database for proper attribution.

## Progress Tracking

Create a spreadsheet or use the Python script to track:
- [ ] Profile researched
- [ ] Photo collected
- [ ] Education details entered
- [ ] Professional details entered
- [ ] LinkedIn profile found
- [ ] Citations documented
- [ ] Database updated

## Notes

- Always verify information from multiple sources
- Prioritize official government sources
- Respect privacy - only use publicly available information
- Include proper citations for all data
- Update `verified_source` field with source URLs
- Mark `updated_at` timestamp after each update

## Next Steps

1. Start with 2019 batch (9 profiles) - highest priority
2. Document research process and refine workflow
3. Create templates for common education/experience patterns
4. Build out comprehensive database
5. Export updated JSON for website deployment
