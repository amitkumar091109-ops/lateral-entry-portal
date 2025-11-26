#!/usr/bin/env python3
"""
Update database with verified 2021 batch data from PIB and add 2023/2024 advertisement info.
Source: https://www.pib.gov.in/Pressreleaseshare.aspx?PRID=1762195
"""

import sqlite3
import json
from datetime import datetime

DB_PATH = "/home/ubuntu/projects/lateral-entry-portal/database/lateral_entry.db"

# Data from PIB Press Release ID 1762195 (Oct 8, 2021)
BATCH_2021_DATA = [
    # Joint Secretaries
    {
        "name": "Samuel Praveen Kumar",
        "post": "Joint Secretary",
        "dept": "Department of Agriculture Cooperation and Farmers Welfare",
        "ministry": "Ministry of Agriculture and Farmers Welfare",
    },
    {
        "name": "Manish Chadha",
        "post": "Joint Secretary",
        "dept": "Department of Commerce",
        "ministry": "Ministry of Commerce and Industry",
    },
    {
        "name": "Balasubramanian Krishnamurthy",
        "post": "Joint Secretary",
        "dept": "Department of Revenue",
        "ministry": "Ministry of Finance",
    },
    # Directors
    {
        "name": "Kapil Ashok Bendre",
        "post": "Director",
        "dept": "Department of Agriculture, Cooperation and Farmers Welfare",
        "ministry": "Ministry of Agriculture and Farmers Welfare",
    },
    {
        "name": "Neeraj Gaba",
        "post": "Director",
        "dept": "Department of Commerce",
        "ministry": "Ministry of Commerce and Industry",
    },
    {
        "name": "Sagar Rameshrao Kadu",
        "post": "Director",
        "dept": "Department of Commerce",
        "ministry": "Ministry of Commerce and Industry",
    },
    {
        "name": "Prabhu Narayan",
        "post": "Director",
        "dept": "Department of Economic Affairs",
        "ministry": "Ministry of Finance",
    },
    {
        "name": "Harsha Bhowmik",
        "post": "Director",
        "dept": "Department of Economic Affairs",
        "ministry": "Ministry of Finance",
    },
    {
        "name": "Shekhar Chaudhary",
        "post": "Director",
        "dept": "Department of Economic Affairs",
        "ministry": "Ministry of Finance",
    },
    {
        "name": "Hardik Mukesh Sheth",
        "post": "Director",
        "dept": "Department of Financial Services",
        "ministry": "Ministry of Finance",
    },
    {
        "name": "Mandakini Balodhi",
        "post": "Director",
        "dept": "Department of Financial Services",
        "ministry": "Ministry of Finance",
    },
    {
        "name": "Avnit Singh Arora",
        "post": "Director",
        "dept": "Department of Legal Affairs",
        "ministry": "Ministry of Law and Justice",
    },
    {
        "name": "Haimanti Bhattacharya",
        "post": "Director",
        "dept": "Department of Legal Affairs",
        "ministry": "Ministry of Law and Justice",
    },
    {
        "name": "Mateshwari Prasad Mishra",
        "post": "Director",
        "dept": "Department of Food and Public Distribution",
        "ministry": "Ministry of Consumer Affairs, Food and Public Distribution",
    },
    {
        "name": "Gaurav Singh",
        "post": "Director",
        "dept": "Department of Higher Education",
        "ministry": "Ministry of Education",
    },
    {
        "name": "Edla Naveen Nicolas",
        "post": "Director",
        "dept": "Department of School Education & Literacy",
        "ministry": "Ministry of Education",
    },
    {
        "name": "Mukta Agarwal",
        "post": "Director",
        "dept": "Department of School Education & Literacy",
        "ministry": "Ministry of Education",
    },
    {
        "name": "Shiv Mohan Dixit",
        "post": "Director",
        "dept": "Department of Water Resources, River Development and Ganga Rejuvenation",
        "ministry": "Ministry of Jal Shakti",
    },
    {
        "name": "Govind Kumar Bansal",
        "post": "Director",
        "dept": "Department of Health & Family Welfare",
        "ministry": "Ministry of Health & Family Welfare",
    },
    {
        "name": "Bidur Kant Jha",
        "post": "Director",
        "dept": "Ministry of Road Transport and Highways",
        "ministry": "Ministry of Road Transport and Highways",
    },
    {
        "name": "Avik Bhattacharyya",
        "post": "Director",
        "dept": "Ministry of Civil Aviation",
        "ministry": "Ministry of Civil Aviation",
    },
    {
        "name": "Sandesh Madhavrao Tilekar",
        "post": "Director",
        "dept": "Ministry of Skill Development & Entrepreneurship",
        "ministry": "Ministry of Skill Development & Entrepreneurship",
    },
    # Deputy Secretaries
    {
        "name": "Reetu Chandra",
        "post": "Deputy Secretary",
        "dept": "Department of School Education and Literacy",
        "ministry": "Ministry of Education",
    },
    {
        "name": "Ruchika Drall",
        "post": "Deputy Secretary",
        "dept": "Ministry of Environment Forests and Climate Change",
        "ministry": "Ministry of Environment Forests and Climate Change",
    },
    {
        "name": "Soumendu Ray",
        "post": "Deputy Secretary",
        "dept": "Ministry of Statistics & Programme Implementation",
        "ministry": "Ministry of Statistics & Programme Implementation",
    },
    {
        "name": "Sarathy Raja G",
        "post": "Deputy Secretary",
        "dept": "Ministry of Steel",
        "ministry": "Ministry of Steel",
    },
    {
        "name": "Rajan Jain",
        "post": "Deputy Secretary",
        "dept": "Ministry of Corporate Affairs",
        "ministry": "Ministry of Corporate Affairs",
    },
    {
        "name": "Dheeraj Kumar",
        "post": "Deputy Secretary",
        "dept": "Ministry of Mines",
        "ministry": "Ministry of Mines",
    },
    {
        "name": "Rajesh Asati",
        "post": "Deputy Secretary",
        "dept": "Ministry of Ports Shipping and Waterways",
        "ministry": "Ministry of Ports Shipping and Waterways",
    },
    {
        "name": "Gaurav Kishor Joshi",
        "post": "Deputy Secretary",
        "dept": "Ministry of Heavy Industries & Public Enterprises",
        "ministry": "Ministry of Heavy Industries & Public Enterprises",
    },
    {
        "name": "Jamiruddin Ansari",
        "post": "Deputy Secretary",
        "dept": "Ministry of Housing and Urban Affairs",
        "ministry": "Ministry of Housing and Urban Affairs",
    },
]


def update_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Updating 2021 Batch Data from PIB...")

    source = "PIB Press Release 1762195 (Oct 8, 2021)"

    for officer in BATCH_2021_DATA:
        # Check if exists
        cursor.execute(
            "SELECT id FROM lateral_entrants WHERE name LIKE ?",
            (f"%{officer['name']}%",),
        )
        existing = cursor.fetchone()

        if existing:
            print(f"Updating existing: {officer['name']}")
            cursor.execute(
                """
                UPDATE lateral_entrants 
                SET position = ?, department = ?, ministry = ?, batch_year = 2021, verified_source = ?
                WHERE id = ?
            """,
                (
                    officer["post"],
                    officer["dept"],
                    officer["ministry"],
                    source,
                    existing[0],
                ),
            )
        else:
            print(f"Inserting new: {officer['name']}")
            cursor.execute(
                """
                INSERT INTO lateral_entrants (name, position, department, ministry, batch_year, verified_source, current_status)
                VALUES (?, ?, ?, ?, 2021, ?, 'Recommended by UPSC')
            """,
                (
                    officer["name"],
                    officer["post"],
                    officer["dept"],
                    officer["ministry"],
                    source,
                ),
            )

    conn.commit()
    print("Database update complete.")
    conn.close()


if __name__ == "__main__":
    update_database()
