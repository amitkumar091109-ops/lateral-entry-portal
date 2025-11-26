#!/usr/bin/env python3
"""
Database Migration Runner
Applies all pending migrations to the lateral_entry database
"""

import sqlite3
import os
from pathlib import Path
from datetime import datetime

# Paths
DB_PATH = Path(__file__).parent / 'lateral_entry.db'
MIGRATIONS_DIR = Path(__file__).parent / 'migrations'

def get_migrations():
    """Get all migration files in order"""
    if not MIGRATIONS_DIR.exists():
        print(f"❌ Migrations directory not found: {MIGRATIONS_DIR}")
        return []

    migrations = sorted([
        f for f in MIGRATIONS_DIR.glob('*.sql')
    ])
    return migrations

def create_migrations_table(conn):
    """Create table to track applied migrations"""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            migration_name VARCHAR(255) UNIQUE NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

def is_migration_applied(conn, migration_name):
    """Check if migration has already been applied"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM schema_migrations WHERE migration_name = ?
    """, (migration_name,))
    return cursor.fetchone()[0] > 0

def apply_migration(conn, migration_file):
    """Apply a single migration file"""
    migration_name = migration_file.name

    if is_migration_applied(conn, migration_name):
        print(f"⏭️  Skipping {migration_name} (already applied)")
        return True

    print(f"📦 Applying {migration_name}...")

    try:
        # Read migration SQL
        with open(migration_file, 'r') as f:
            sql = f.read()

        # Execute entire SQL script using executescript()
        cursor = conn.cursor()
        try:
            cursor.executescript(sql)
        except sqlite3.OperationalError as e:
            # Handle specific known errors that are acceptable
            if 'duplicate column name' in str(e).lower() or 'already exists' in str(e).lower():
                print(f"   ⚠️  Column/table already exists (continuing...): {str(e)[:100]}")
            else:
                raise

        # Record migration as applied
        cursor.execute("""
            INSERT INTO schema_migrations (migration_name) VALUES (?)
        """, (migration_name,))

        conn.commit()
        print(f"✅ Successfully applied {migration_name}")
        return True

    except Exception as e:
        print(f"❌ Error applying {migration_name}: {e}")
        conn.rollback()
        return False

def main():
    """Main migration runner"""
    print("=" * 60)
    print("🔧 Lateral Entry Database Migration Runner")
    print("=" * 60)
    print()

    # Check database exists
    if not DB_PATH.exists():
        print(f"❌ Database not found: {DB_PATH}")
        print("   Please run init_database.py first")
        return

    # Get migrations
    migrations = get_migrations()
    if not migrations:
        print("❌ No migration files found")
        return

    print(f"📋 Found {len(migrations)} migration(s):\n")
    for m in migrations:
        print(f"   • {m.name}")
    print()

    # Connect to database
    print(f"🔗 Connecting to database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        # Create migrations tracking table
        create_migrations_table(conn)

        # Apply each migration
        print("\n🚀 Starting migrations...\n")
        success_count = 0

        for migration_file in migrations:
            if apply_migration(conn, migration_file):
                success_count += 1
            print()  # Blank line between migrations

        # Summary
        print("=" * 60)
        print(f"✨ Migration complete!")
        print(f"   Applied: {success_count}/{len(migrations)} migrations")
        print("=" * 60)

        # Show table count
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"\n📊 Total tables in database: {len(tables)}")

        # Show new authentication tables
        auth_tables = [t for t in tables if t in [
            'users', 'pending_users', 'sessions', 'admin_settings', 'audit_log',
            'field_visibility_settings', 'uploads', 'field_edit_requests',
            'job_listings', 'user_job_preferences', 'saved_jobs'
        ]]

        if auth_tables:
            print("\n✅ New tables created:")
            for table in auth_tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   • {table}: {count} rows")

    finally:
        conn.close()
        print("\n🔒 Database connection closed")

if __name__ == '__main__':
    main()
