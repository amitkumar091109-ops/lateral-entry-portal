-- Government of India Lateral Entry Portal Database Schema
-- This database stores comprehensive information about lateral entrants across three batches

-- Main lateral entrants table
CREATE TABLE IF NOT EXISTS lateral_entrants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    batch_year INTEGER NOT NULL, -- 2019, 2021, 2024
    position VARCHAR(255) NOT NULL,
    department VARCHAR(255) NOT NULL,
    ministry VARCHAR(255),
    state VARCHAR(100),
    photo_url TEXT,
    profile_summary TEXT,
    educational_background TEXT,
    previous_experience TEXT,
    date_of_appointment DATE,
    retirement_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Detailed professional information
CREATE TABLE IF NOT EXISTS professional_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entrant_id INTEGER,
    previous_company TEXT,
    previous_position VARCHAR(255),
    industry_sector VARCHAR(255),
    years_experience INTEGER,
    domain_expertise TEXT,
    achievements TEXT,
    FOREIGN KEY (entrant_id) REFERENCES lateral_entrants(id)
);

-- Educational background details
CREATE TABLE IF NOT EXISTS education_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entrant_id INTEGER,
    degree_type VARCHAR(100), -- PhD, Master's, Bachelor's, etc.
    degree_name VARCHAR(255),
    institution VARCHAR(255),
    specialization VARCHAR(255),
    year_of_completion INTEGER,
    university_rank INTEGER,
    FOREIGN KEY (entrant_id) REFERENCES lateral_entrants(id)
);

-- Media coverage and news articles
CREATE TABLE IF NOT EXISTS media_coverage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entrant_id INTEGER,
    source_name VARCHAR(255), -- Times of India, Economic Times, etc.
    article_title VARCHAR(500),
    article_url TEXT,
    publication_date DATE,
    news_type VARCHAR(100), -- Appointment, Achievement, Interview, etc.
    content_summary TEXT,
    FOREIGN KEY (entrant_id) REFERENCES lateral_entrants(id)
);

-- Social media profiles
CREATE TABLE IF NOT EXISTS social_media_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entrant_id INTEGER,
    platform VARCHAR(100), -- LinkedIn, Twitter, etc.
    profile_url TEXT,
    follower_count INTEGER,
    verified BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (entrant_id) REFERENCES lateral_entrants(id)
);

-- Performance and achievements
CREATE TABLE IF NOT EXISTS achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entrant_id INTEGER,
    achievement_type VARCHAR(100), -- Policy, Innovation, Reform, etc.
    achievement_title VARCHAR(255),
    achievement_description TEXT,
    impact_measure TEXT,
    recognition_received TEXT,
    FOREIGN KEY (entrant_id) REFERENCES lateral_entrants(id)
);

-- Contact information
CREATE TABLE IF NOT EXISTS contact_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entrant_id INTEGER,
    email VARCHAR(255),
    phone VARCHAR(50),
    official_address TEXT,
    personal_address TEXT,
    FOREIGN KEY (entrant_id) REFERENCES lateral_entrants(id)
);

-- Search and filter categories
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT
);

-- Department-wise categorization
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name VARCHAR(255) NOT NULL UNIQUE,
    ministry VARCHAR(255),
    description TEXT
);

-- Linking entrants to categories
CREATE TABLE IF NOT EXISTS entrant_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entrant_id INTEGER,
    category_id INTEGER,
    FOREIGN KEY (entrant_id) REFERENCES lateral_entrants(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Insert initial categories
INSERT OR IGNORE INTO categories (category_name, description) VALUES 
('Finance & Banking', 'Financial sector experts and bankers'),
('Technology & Innovation', 'Technology leaders and innovators'),
('Public Policy', 'Policy experts and researchers'),
('Human Resources', 'HR professionals and administrators'),
('Legal Affairs', 'Legal professionals and experts'),
('Healthcare', 'Healthcare sector experts'),
('Education', 'Education sector professionals'),
('Infrastructure', 'Infrastructure and construction experts'),
('Energy & Environment', 'Energy and environmental experts'),
('Agriculture', 'Agricultural sector professionals');

-- Insert department data
INSERT OR IGNORE INTO departments (department_name, ministry, description) VALUES 
('Department of Economic Affairs', 'Ministry of Finance', 'Handles economic policy and financial matters'),
('Department of Information Technology', 'Ministry of Electronics and IT', 'Manages technology policies and digital India'),
('Department of Health & Family Welfare', 'Ministry of Health & Family Welfare', 'Healthcare policy and implementation'),
('Department of School Education', 'Ministry of Education', 'Education policy and school education'),
('Department of Higher Education', 'Ministry of Education', 'Higher education policy and institutions'),
('Department of Infrastructure', 'Ministry of Housing & Urban Affairs', 'Infrastructure development and urban planning'),
('Department of Renewable Energy', 'Ministry of New and Renewable Energy', 'Renewable energy policies and projects'),
('Department of Agriculture', 'Ministry of Agriculture & Farmers Welfare', 'Agricultural policy and farmer welfare'),
('Department of Industry', 'Ministry of Commerce and Industry', 'Industrial policy and manufacturing'),
('Department of Environment', 'Ministry of Environment, Forest and Climate Change', 'Environmental policy and climate change');

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_batch_year ON lateral_entrants(batch_year);
CREATE INDEX IF NOT EXISTS idx_department ON lateral_entrants(department);
CREATE INDEX IF NOT EXISTS idx_ministry ON lateral_entrants(ministry);
CREATE INDEX IF NOT EXISTS idx_name ON lateral_entrants(name);
CREATE INDEX IF NOT EXISTS idx_professional_entrant ON professional_details(entrant_id);
CREATE INDEX IF NOT EXISTS idx_education_entrant ON education_details(entrant_id);
CREATE INDEX IF NOT EXISTS idx_media_entrant ON media_coverage(entrant_id);
CREATE INDEX IF NOT EXISTS idx_social_entrant ON social_media_profiles(entrant_id);
CREATE INDEX IF NOT EXISTS idx_achievements_entrant ON achievements(entrant_id);
CREATE INDEX IF NOT EXISTS idx_contact_entrant ON contact_info(entrant_id);