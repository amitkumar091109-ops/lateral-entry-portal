#!/usr/bin/env python3
"""
Data Collection and Web Scraping Utilities for Lateral Entry Portal
"""

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from datetime import datetime, timedelta
import time
import random
from pathlib import Path

class DataCollection:
    """Handles data collection from various sources"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_news_articles(self, search_term="lateral entry government india", max_articles=50):
        """Scrape news articles about lateral entrants"""
        print(f"Scraping news articles for: {search_term}")
        
        # Note: In a real implementation, you would use proper news APIs
        # This is a demonstration with sample data structure
        
        sample_articles = [
            {
                "title": "Government announces new batch of lateral entrants",
                "source": "Times of India",
                "url": "https://timesofindia.indiatimes.com/news/politics",
                "date": "2024-01-15",
                "summary": "The Government of India announced 10 new lateral entrants across various ministries."
            },
            {
                "title": "Lateral entry appointments: A comprehensive analysis",
                "source": "Economic Times",
                "url": "https://economictimes.indiatimes.com/news/politics",
                "date": "2024-01-10",
                "summary": "Analysis of the latest batch of lateral entrants and their qualifications."
            },
            {
                "title": "ISRO Chairman S. Somanath's journey to space leadership",
                "source": "The Hindu",
                "url": "https://www.thehindu.com/sci-tech/science",
                "date": "2023-08-23",
                "summary": "Profile of ISRO Chairman and his contributions to India's space program."
            }
        ]
        
        return sample_articles[:max_articles]
    
    def validate_entrant_data(self, entrant_data):
        """Validate entrant data for completeness and accuracy"""
        required_fields = ['name', 'batch_year', 'position', 'department', 'ministry']
        optional_fields = ['state', 'educational_background', 'previous_experience']
        
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Check required fields
        for field in required_fields:
            if not entrant_data.get(field):
                validation_result['errors'].append(f"Missing required field: {field}")
                validation_result['is_valid'] = False
        
        # Check optional fields
        for field in optional_fields:
            if not entrant_data.get(field):
                validation_result['warnings'].append(f"Missing optional field: {field}")
        
        # Validate batch year
        batch_year = entrant_data.get('batch_year')
        if batch_year and batch_year not in [2019, 2021, 2024]:
            validation_result['errors'].append(f"Invalid batch year: {batch_year}")
            validation_result['is_valid'] = False
        
        # Validate date format
        date_str = entrant_data.get('date_of_appointment')
        if date_str:
            try:
                datetime.strptime(str(date_str), '%Y-%m-%d')
            except ValueError:
                validation_result['warnings'].append(f"Invalid date format: {date_str}")
        
        return validation_result
    
    def standardize_names(self, name):
        """Standardize name format for consistency"""
        if not name:
            return ""
        
        # Remove extra spaces and proper case
        name = ' '.join(name.strip().split())
        return name.title()
    
    def get_photo_suggestions(self, entrant_name, position, department):
        """Generate suggestions for photo search keywords"""
        search_keywords = [
            f"{entrant_name} {position}",
            f"{entrant_name} government india",
            f"{entrant_name} {department}",
            f"{entrant_name} civil servant",
            f"{entrant_name} bureaucrat"
        ]
        
        # Add LinkedIn, government websites, and news sources
        photo_sources = [
            "linkedin.com",
            "government websites",
            "news articles",
            "press conferences",
            "official photographs"
        ]
        
        return {
            'search_keywords': search_keywords,
            'suggested_sources': photo_sources
        }
    
    def generate_entrant_report(self, entrant_data):
        """Generate comprehensive report for an entrant"""
        report = {
            'entrant_info': entrant_data,
            'data_quality_score': self.calculate_quality_score(entrant_data),
            'photo_search_suggestions': self.get_photo_suggestions(
                entrant_data['name'], 
                entrant_data['position'], 
                entrant_data['department']
            ),
            'verification_status': self.verify_entrant_info(entrant_data),
            'last_updated': datetime.now().isoformat()
        }
        
        return report
    
    def calculate_quality_score(self, entrant_data):
        """Calculate data quality score (0-100)"""
        score = 0
        total_fields = 15
        
        # Required fields (40 points)
        required_fields = ['name', 'batch_year', 'position', 'department', 'ministry']
        for field in required_fields:
            if entrant_data.get(field):
                score += 8
        
        # Important optional fields (30 points)
        optional_fields = ['state', 'educational_background', 'previous_experience', 'date_of_appointment']
        for field in optional_fields:
            if entrant_data.get(field):
                score += 7.5
        
        # Additional information (20 points)
        additional_fields = ['profile_summary', 'photo_url']
        for field in additional_fields:
            if entrant_data.get(field):
                score += 10
        
        # Media coverage (10 points)
        if 'media_coverage' in entrant_data and entrant_data['media_coverage']:
            score += 10
        
        return min(score, 100)
    
    def verify_entrant_info(self, entrant_data):
        """Basic verification of entrant information"""
        verification = {
            'status': 'pending',
            'checks_performed': [],
            'confidence_level': 0.5
        }
        
        # Check name validity
        name = entrant_data.get('name', '')
        if len(name.split()) >= 2:  # At least first and last name
            verification['checks_performed'].append('Name format validated')
            verification['confidence_level'] += 0.1
        
        # Check batch year consistency
        batch_year = entrant_data.get('batch_year')
        appointment_date = entrant_data.get('date_of_appointment')
        
        if batch_year and appointment_date:
            try:
                app_year = int(appointment_date.split('-')[0])
                if abs(app_year - batch_year) <= 1:  # Allow 1 year difference
                    verification['checks_performed'].append('Batch year and appointment date consistent')
                    verification['confidence_level'] += 0.2
            except:
                pass
        
        # Check department-ministry consistency
        dept = entrant_data.get('department', '').lower()
        ministry = entrant_data.get('ministry', '').lower()
        
        # Known mappings
        dept_ministry_map = {
            'economic': 'finance',
            'information': 'electronics',
            'health': 'health',
            'education': 'education',
            'commerce': 'commerce',
            'renewable': 'new and renewable energy'
        }
        
        for dept_key, ministry_key in dept_ministry_map.items():
            if dept_key in dept and ministry_key in ministry:
                verification['checks_performed'].append('Department-ministry mapping verified')
                verification['confidence_level'] += 0.2
                break
        
        verification['status'] = 'verified' if verification['confidence_level'] > 0.7 else 'pending'
        return verification
    
    def export_data_collection_report(self, entrants_data, output_path):
        """Export comprehensive data collection report"""
        report = {
            'collection_summary': {
                'total_entrants': len(entrants_data),
                'collection_date': datetime.now().isoformat(),
                'data_sources': ['government announcements', 'news media', 'official sources']
            },
            'quality_analysis': {
                'average_quality_score': 0,
                'high_quality_count': 0,
                'low_quality_count': 0
            },
            'entrants_report': []
        }
        
        quality_scores = []
        for entrant_data in entrants_data:
            entrant_report = self.generate_entrant_report(entrant_data)
            report['entrants_report'].append(entrant_report)
            quality_scores.append(entrant_report['data_quality_score'])
        
        if quality_scores:
            report['quality_analysis']['average_quality_score'] = sum(quality_scores) / len(quality_scores)
            report['quality_analysis']['high_quality_count'] = len([s for s in quality_scores if s >= 80])
            report['quality_analysis']['low_quality_count'] = len([s for s in quality_scores if s < 50])
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str)
        
        return report

def main():
    """Demonstrate data collection utilities"""
    collector = DataCollection()
    
    print("=" * 60)
    print("Data Collection and Validation System")
    print("=" * 60)
    
    # Sample entrant data for validation
    sample_entrant = {
        "name": "Dr. Rajesh Kumar",
        "batch_year": 2024,
        "position": "Secretary",
        "department": "Department of Renewable Energy",
        "ministry": "Ministry of New and Renewable Energy",
        "state": "Karnataka",
        "educational_background": "B.Tech from NIT Surathkal",
        "previous_experience": "Additional Secretary MNRE",
        "date_of_appointment": "2024-02-01",
        "profile_summary": "Expert in renewable energy policy"
    }
    
    # Validate data
    print("\n🔍 Validating sample entrant data:")
    validation = collector.validate_entrant_data(sample_entrant)
    print(f"Valid: {validation['is_valid']}")
    if validation['errors']:
        print(f"Errors: {validation['errors']}")
    if validation['warnings']:
        print(f"Warnings: {validation['warnings']}")
    
    # Generate quality score
    quality_score = collector.calculate_quality_score(sample_entrant)
    print(f"Quality Score: {quality_score}/100")
    
    # Get photo search suggestions
    photo_suggestions = collector.get_photo_suggestions(
        sample_entrant['name'], 
        sample_entrant['position'], 
        sample_entrant['department']
    )
    print(f"\n📸 Photo search suggestions:")
    for keyword in photo_suggestions['search_keywords'][:3]:
        print(f"  - {keyword}")
    
    # Scrape news articles
    print(f"\n📰 Scraping news articles:")
    articles = collector.scrape_news_articles(max_articles=5)
    print(f"Found {len(articles)} articles")
    for article in articles[:3]:
        print(f"  - {article['title']} ({article['source']})")
    
    # Generate export report
    export_path = "/home/ubuntu/projects/lateral-entry-portal/data/collection_report.json"
    report = collector.export_data_collection_report([sample_entrant], export_path)
    print(f"\n📊 Collection report saved to: {export_path}")
    
    print(f"\n✅ Data collection demonstration completed!")

if __name__ == "__main__":
    main()