#!/usr/bin/env python3
"""
Lateral Entry Portal - Data Management System
This script provides comprehensive database operations and analytics
"""

import sqlite3
import json
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class LateralEntryDataManager:
    def __init__(self, db_path="/home/ubuntu/projects/lateral-entry-portal/database/lateral_entry.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with schema"""
        conn = sqlite3.connect(self.db_path)
        with open('/home/ubuntu/projects/lateral-entry-portal/database/lateral_entry_schema.sql', 'r') as schema_file:
            schema_sql = schema_file.read()
            conn.executescript(schema_sql)
        conn.close()
    
    def connect(self):
        """Create database connection"""
        return sqlite3.connect(self.db_path)
    
    def get_all_entrants(self):
        """Get all lateral entrants with basic information"""
        conn = self.connect()
        query = """
        SELECT le.*, 
               GROUP_CONCAT(c.category_name) as categories,
               COUNT(mc.id) as media_count
        FROM lateral_entrants le
        LEFT JOIN entrant_categories ec ON le.id = ec.entrant_id
        LEFT JOIN categories c ON ec.category_id = c.id
        LEFT JOIN media_coverage mc ON le.id = mc.entrant_id
        GROUP BY le.id
        ORDER BY le.batch_year DESC, le.name ASC
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def get_entrants_by_batch(self, batch_year):
        """Get entrants filtered by batch year"""
        conn = self.connect()
        query = """
        SELECT le.*, 
               GROUP_CONCAT(c.category_name) as categories,
               COUNT(mc.id) as media_count
        FROM lateral_entrants le
        LEFT JOIN entrant_categories ec ON le.id = ec.entrant_id
        LEFT JOIN categories c ON ec.category_id = c.id
        LEFT JOIN media_coverage mc ON le.id = mc.entrant_id
        WHERE le.batch_year = ?
        GROUP BY le.id
        ORDER BY le.name ASC
        """
        df = pd.read_sql_query(query, conn, params=(batch_year,))
        conn.close()
        return df
    
    def search_entrants(self, search_term):
        """Search entrants by name, position, department, or ministry"""
        conn = self.connect()
        search_pattern = f"%{search_term}%"
        query = """
        SELECT le.*, 
               GROUP_CONCAT(c.category_name) as categories,
               COUNT(mc.id) as media_count
        FROM lateral_entrants le
        LEFT JOIN entrant_categories ec ON le.id = ec.entrant_id
        LEFT JOIN categories c ON ec.category_id = c.id
        LEFT JOIN media_coverage mc ON le.id = mc.entrant_id
        WHERE le.name LIKE ? OR 
              le.position LIKE ? OR 
              le.department LIKE ? OR 
              le.ministry LIKE ? OR
              le.profile_summary LIKE ?
        GROUP BY le.id
        ORDER BY le.batch_year DESC, le.name ASC
        """
        df = pd.read_sql_query(query, conn, params=(search_pattern, search_pattern, 
                                                   search_pattern, search_pattern, search_pattern))
        conn.close()
        return df
    
    def get_entrants_by_category(self, category_name):
        """Get entrants filtered by category"""
        conn = self.connect()
        query = """
        SELECT le.*, 
               GROUP_CONCAT(c.category_name) as categories,
               COUNT(mc.id) as media_count
        FROM lateral_entrants le
        JOIN entrant_categories ec ON le.id = ec.entrant_id
        JOIN categories c ON ec.category_id = c.id
        LEFT JOIN media_coverage mc ON le.id = mc.entrant_id
        WHERE c.category_name = ?
        GROUP BY le.id
        ORDER BY le.batch_year DESC, le.name ASC
        """
        df = pd.read_sql_query(query, conn, params=(category_name,))
        conn.close()
        return df
    
    def get_detailed_profile(self, entrant_id):
        """Get detailed profile of an entrant"""
        conn = self.connect()
        
        # Basic info
        basic_query = "SELECT * FROM lateral_entrants WHERE id = ?"
        basic_info = pd.read_sql_query(basic_query, conn, params=(entrant_id,))
        
        # Professional details
        prof_query = """
        SELECT pd.* FROM professional_details pd 
        WHERE pd.entrant_id = ?
        """
        professional = pd.read_sql_query(prof_query, conn, params=(entrant_id,))
        
        # Education details
        edu_query = """
        SELECT ed.* FROM education_details ed 
        WHERE ed.entrant_id = ?
        """
        education = pd.read_sql_query(edu_query, conn, params=(entrant_id,))
        
        # Media coverage
        media_query = """
        SELECT mc.* FROM media_coverage mc 
        WHERE mc.entrant_id = ?
        ORDER BY mc.publication_date DESC
        """
        media = pd.read_sql_query(media_query, conn, params=(entrant_id,))
        
        # Social media profiles
        social_query = """
        SELECT smp.* FROM social_media_profiles smp 
        WHERE smp.entrant_id = ?
        """
        social = pd.read_sql_query(social_query, conn, params=(entrant_id,))
        
        # Achievements
        ach_query = """
        SELECT a.* FROM achievements a 
        WHERE a.entrant_id = ?
        """
        achievements = pd.read_sql_query(ach_query, conn, params=(entrant_id,))
        
        conn.close()
        
        return {
            'basic_info': basic_info,
            'professional': professional,
            'education': education,
            'media': media,
            'social': social,
            'achievements': achievements
        }
    
    def get_statistics(self):
        """Get comprehensive statistics"""
        conn = self.connect()
        
        stats = {}
        
        # Total entrants
        stats['total_entrants'] = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM lateral_entrants", conn).iloc[0]['count']
        
        # By batch
        stats['by_batch'] = pd.read_sql_query("""
            SELECT batch_year, COUNT(*) as count 
            FROM lateral_entrants 
            GROUP BY batch_year 
            ORDER BY batch_year
        """, conn)
        
        # By ministry
        stats['by_ministry'] = pd.read_sql_query("""
            SELECT ministry, COUNT(*) as count 
            FROM lateral_entrants 
            GROUP BY ministry 
            ORDER BY count DESC
        """, conn)
        
        # By department
        stats['by_department'] = pd.read_sql_query("""
            SELECT department, COUNT(*) as count 
            FROM lateral_entrants 
            GROUP BY department 
            ORDER BY count DESC
        """, conn)
        
        # By state
        stats['by_state'] = pd.read_sql_query("""
            SELECT state, COUNT(*) as count 
            FROM lateral_entrants 
            GROUP BY state 
            ORDER BY count DESC
        """, conn)
        
        # Media coverage statistics
        stats['media_coverage'] = pd.read_sql_query("""
            SELECT mc.source_name, COUNT(*) as article_count,
                   AVG(CASE WHEN length(mc.article_title) > 0 THEN 1 ELSE 0 END) as coverage_rate
            FROM media_coverage mc
            GROUP BY mc.source_name
            ORDER BY article_count DESC
        """, conn)
        
        # Categories distribution
        stats['by_category'] = pd.read_sql_query("""
            SELECT c.category_name, COUNT(ec.entrant_id) as count
            FROM categories c
            LEFT JOIN entrant_categories ec ON c.id = ec.category_id
            GROUP BY c.id, c.category_name
            ORDER BY count DESC
        """, conn)
        
        conn.close()
        return stats
    
    def add_entrant(self, entrant_data):
        """Add a new lateral entrant"""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            # Insert basic information
            cursor.execute("""
                INSERT INTO lateral_entrants 
                (name, batch_year, position, department, ministry, state, 
                 educational_background, previous_experience, date_of_appointment, 
                 profile_summary) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entrant_data['name'], entrant_data['batch_year'], entrant_data['position'],
                entrant_data['department'], entrant_data['ministry'], entrant_data['state'],
                entrant_data.get('educational_background', ''), 
                entrant_data.get('previous_experience', ''),
                entrant_data.get('date_of_appointment', datetime.now().date()),
                entrant_data.get('profile_summary', '')
            ))
            
            entrant_id = cursor.lastrowid
            
            # Insert professional details if provided
            if 'professional' in entrant_data:
                prof = entrant_data['professional']
                cursor.execute("""
                    INSERT INTO professional_details 
                    (entrant_id, previous_company, previous_position, industry_sector, 
                     years_experience, domain_expertise, achievements) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    entrant_id, prof.get('previous_company', ''), prof.get('previous_position', ''),
                    prof.get('industry_sector', ''), prof.get('years_experience', 0),
                    prof.get('domain_expertise', ''), prof.get('achievements', '')
                ))
            
            # Insert media coverage if provided
            if 'media_coverage' in entrant_data:
                for media in entrant_data['media_coverage']:
                    cursor.execute("""
                        INSERT INTO media_coverage 
                        (entrant_id, source_name, article_title, publication_date, 
                         news_type, content_summary) 
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        entrant_id, media.get('source_name', ''), media.get('article_title', ''),
                        media.get('publication_date', datetime.now().date()),
                        media.get('news_type', ''), media.get('content_summary', '')
                    ))
            
            conn.commit()
            return entrant_id
        
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def export_to_json(self, output_path="/home/ubuntu/projects/lateral-entry-portal/data/export.json"):
        """Export all data to JSON format"""
        entrants = self.get_all_entrants().to_dict('records')
        
        # Convert DataFrames to lists
        stats = self.get_statistics()
        stats_dict = {}
        for key, value in stats.items():
            if isinstance(value, pd.DataFrame):
                stats_dict[key] = value.to_dict('records')
            else:
                stats_dict[key] = value
        
        export_data = {
            'entrants': entrants,
            'statistics': stats_dict,
            'export_date': datetime.now().isoformat(),
            'total_records': len(entrants)
        }
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        return output_path
    
    def create_visualizations(self, output_dir="/home/ubuntu/projects/lateral-entry-portal/analytics/"):
        """Create visualization charts"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        stats = self.get_statistics()
        
        # Set style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # 1. Batch Distribution Pie Chart
        fig, ax = plt.subplots(figsize=(10, 8))
        batch_counts = stats['by_batch']['count']
        batch_years = stats['by_batch']['batch_year']
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        ax.pie(batch_counts, labels=batch_years, autopct='%1.1f%%', colors=colors, startangle=90)
        ax.set_title('Distribution of Lateral Entrants by Batch Year', fontsize=16, fontweight='bold')
        plt.savefig(f"{output_dir}/batch_distribution.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Top Ministries Bar Chart
        fig, ax = plt.subplots(figsize=(12, 8))
        top_ministries = stats['by_ministry'].head(8)
        sns.barplot(data=top_ministries, y='ministry', x='count', ax=ax)
        ax.set_title('Top Ministries by Number of Lateral Entrants', fontsize=16, fontweight='bold')
        ax.set_xlabel('Number of Entrants')
        plt.tight_layout()
        plt.savefig(f"{output_dir}/ministry_distribution.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. State Distribution
        fig, ax = plt.subplots(figsize=(10, 6))
        state_counts = stats['by_state'].head(10)
        sns.barplot(data=state_counts, y='state', x='count', ax=ax)
        ax.set_title('Top States by Number of Lateral Entrants', fontsize=16, fontweight='bold')
        ax.set_xlabel('Number of Entrants')
        plt.tight_layout()
        plt.savefig(f"{output_dir}/state_distribution.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        # 4. Category Distribution
        fig, ax = plt.subplots(figsize=(10, 8))
        category_data = stats['by_category'][stats['by_category']['count'] > 0]
        if not category_data.empty:
            sns.barplot(data=category_data, y='category_name', x='count', ax=ax)
            ax.set_title('Distribution by Professional Categories', fontsize=16, fontweight='bold')
            ax.set_xlabel('Number of Entrants')
            plt.tight_layout()
            plt.savefig(f"{output_dir}/category_distribution.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Visualizations saved to {output_dir}")
        return output_dir

def main():
    """Main function to demonstrate usage"""
    manager = LateralEntryDataManager()
    
    print("=" * 60)
    print("India Lateral Entry Portal - Data Management System")
    print("=" * 60)
    
    # Get basic statistics
    stats = manager.get_statistics()
    print(f"\n📊 PORTAL STATISTICS:")
    print(f"Total Entrants: {stats['total_entrants']}")
    print(f"Batches: {stats['by_batch']['batch_year'].tolist()}")
    print(f"Total Ministries: {len(stats['by_ministry'])}")
    print(f"Total Departments: {len(stats['by_department'])}")
    
    # Display batch distribution
    print(f"\n📈 BATCH DISTRIBUTION:")
    for _, row in stats['by_batch'].iterrows():
        print(f"  {row['batch_year']}: {row['count']} entrants")
    
    # Display top ministries
    print(f"\n🏛️ TOP MINISTRIES:")
    for _, row in stats['by_ministry'].head(5).iterrows():
        print(f"  {row['ministry']}: {row['count']} entrants")
    
    # Export data
    export_path = manager.export_to_json()
    print(f"\n💾 Data exported to: {export_path}")
    
    # Create visualizations
    viz_path = manager.create_visualizations()
    print(f"\n📊 Visualizations created in: {viz_path}")
    
    # Sample search
    print(f"\n🔍 SAMPLE SEARCH (Technology):")
    tech_entrants = manager.get_entrants_by_category('Technology & Innovation')
    print(f"Found {len(tech_entrants)} technology-related entrants:")
    for _, entrant in tech_entrants.iterrows():
        print(f"  - {entrant['name']} ({entrant['position']})")
    
    print(f"\n✅ Database operations completed successfully!")

if __name__ == "__main__":
    main()