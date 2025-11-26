# 2021 Batch Duplicate Entries Analysis

## Summary
Found **3 duplicate entries** in the 2021 batch:
- Current count: **36 entries**
- Should be: **33 unique appointees**
- Action needed: **Delete 3 duplicate records**

---

## Duplicate #1: Govind Kumar Bansal / Govind K Bansal

### Entry 1 (KEEP - ID: 61)
- **Name:** Govind K Bansal
- **Ministry:** Ministry of Health and Family Welfare
- **Position:** Director
- **Date:** 2021-12-30
- **Extension:** 2025-12-30
- **Status:** Active - Extended Term
- **Source:** The Secretariat article (Dec 19, 2024)
- **Why keep:** More recent, has extension info, better source

### Entry 2 (DELETE - ID: 34)
- **Name:** Govind Kumar Bansal
- **Ministry:** Ministry of Health & Family Welfare
- **Position:** Director
- **Date:** 2021-08-01
- **Extension:** None
- **Status:** None
- **Source:** PIB Press Release 1762195 (Oct 8, 2021)
- **Why delete:** Older entry, no extension data, less complete

---

## Duplicate #2: Haimanti Bhattacharya / Haimanti Bhattacharyya

### Entry 1 (KEEP - ID: 32)
- **Name:** Haimanti Bhattacharya
- **Ministry:** Ministry of Law and Justice
- **Department:** Department of Legal Affairs
- **Position:** Director
- **Date:** 2022-01-11
- **Extension:** 2026-01-11
- **Status:** Active - Extended Term
- **Source:** PIB Press Release 1762195 (Oct 8, 2021)
- **Why keep:** Has extension info, confirmed department, active status

### Entry 2 (DELETE - ID: 54)
- **Name:** Haimanti Bhattacharyya
- **Ministry:** Ministry of Electronics and IT
- **Department:** Cyber Laws Division
- **Position:** Director
- **Date:** 2022-09-01
- **Extension:** None
- **Status:** None
- **Source:** None
- **Why delete:** Different ministry (likely error), no source, no extension

**Note:** The spelling "Bhattacharya" vs "Bhattacharyya" is the same person (common Bengali name variant)

---

## Duplicate #3: G. Sarathy Raja / Sarathy Raja G

### Entry 1 (KEEP - ID: 45)
- **Name:** G. Sarathy Raja
- **Ministry:** Ministry of Steel
- **Department:** Department of Steel
- **Position:** Deputy Secretary
- **Date:** 2022-02-06
- **Extension:** 2027-02-06
- **Status:** Active - Extended Term
- **Source:** The Secretariat article (Dec 19, 2024)
- **Why keep:** Has appointment date, extension info, better source

### Entry 2 (DELETE - ID: 62)
- **Name:** Sarathy Raja G
- **Ministry:** Ministry of Steel
- **Position:** Deputy Secretary
- **Date:** None
- **Extension:** None
- **Status:** Recommended by UPSC
- **Source:** PIB Press Release 1762195 (Oct 8, 2021)
- **Why delete:** No appointment date, incomplete data, just "recommended"

---

## Recommended SQL Commands

```sql
-- Delete the 3 duplicate entries
DELETE FROM lateral_entrants WHERE id = 34;  -- Govind Kumar Bansal duplicate
DELETE FROM lateral_entrants WHERE id = 54;  -- Haimanti Bhattacharyya duplicate  
DELETE FROM lateral_entrants WHERE id = 62;  -- Sarathy Raja G duplicate

-- Verify the cleanup
SELECT COUNT(*) FROM lateral_entrants WHERE batch_year = 2021;
-- Should return: 33

-- Verify no more duplicates
SELECT name, COUNT(*) as count 
FROM lateral_entrants 
WHERE batch_year = 2021 
GROUP BY name 
HAVING COUNT(*) > 1;
-- Should return: empty result
```

---

## Additional Actions Needed

1. **Check related tables** - Ensure no orphaned records in:
   - professional_details
   - education_details
   - media_coverage
   - social_media_profiles
   - achievements
   - contact_info

2. **Update API data export**:
   - Run: `./export_static_data.sh`
   - Deploy updated JSON files

3. **Update total count**:
   - Total should be: **69 appointees** (9 + 33 + 27)
   - Currently showing: **72 appointees** (9 + 36 + 27)

4. **Verify website displays correct counts**:
   - https://prabhu.app/lateral-entry/
   - https://prabhu.app/lateral-entry/pages/profiles.html
   - https://prabhu.app/lateral-entry/pages/batch-2021.html

---

## Root Cause

The duplicates occurred because:
1. Different sources used slightly different name formats
2. Some entries from PIB press releases (recommendations) vs. actual appointments
3. Data was added from multiple sources without deduplication check

## Prevention

Add unique constraint or check before insertion:
```sql
CREATE UNIQUE INDEX idx_unique_entrant 
ON lateral_entrants(name, batch_year, position);
```

