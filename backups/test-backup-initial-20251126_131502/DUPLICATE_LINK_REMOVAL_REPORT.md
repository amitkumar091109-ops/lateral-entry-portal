# Duplicate Link Removal Report

**Date:** November 26, 2025
**Issue:** Duplicate "View Advertisement No. 51/2021" link on history page
**Status:** ✅ FIXED AND DEPLOYED

## Problem

After replacing "Advertisement No. 47/2020" with "Advertisement No. 51/2021", the history page had TWO links for "51/2021":

1. **Duplicate (Removed):** "View Advertisement No. 51/2021" 
   - URL: https://upsc.gov.in/sites/default/files/Advt-Spl-47-LateralEntry-21022021-engl.pdf
   - Problem: URL still pointed to old 47/2020 PDF, but text said "51/2021"
   - Icon: External link (fas fa-external-link-alt)

2. **Kept:** "View Advt No. 51/2021 (RGU)"
   - URL: ../assets/pdfs/2021-advertisement.pdf
   - Correct local PDF link
   - Icon: PDF (fas fa-file-pdf)

## Solution

Removed the duplicate link (lines 75-78) from the 2021 timeline section in history.html.

### Before (4 occurrences of "51/2021"):
- Line 63: Timeline entry text
- Line 67: Advertisement details list
- Line 76: **DUPLICATE LINK** (removed)
- Line 80: Correct PDF link (kept)

### After (3 occurrences of "51/2021"):
- Line 63: Timeline entry text
- Line 67: Advertisement details list
- Line 76: Correct PDF link (kept)

## Code Change

**File:** `pages/history.html` (Lines 74-82)

**Removed:**
```html
<a href="https://upsc.gov.in/sites/default/files/Advt-Spl-47-LateralEntry-21022021-engl.pdf" target="_blank" class="text-theme-accent hover:underline text-sm inline-block">
    <i class="fas fa-external-link-alt mr-1"></i> View Advertisement No. 51/2021
</a>
<br>
```

**Kept:**
```html
<a href="../assets/pdfs/2021-advertisement.pdf" target="_blank" class="text-theme-accent hover:underline text-sm inline-block">
    <i class="fas fa-file-pdf mr-1"></i> View Advt No. 51/2021 (RGU)
</a>
```

## Files Updated

### Local:
✅ `/home/ubuntu/projects/lateral-entry-portal/pages/history.html`

### Production:
✅ `/var/www/html/lateral-entry/pages/history.html`

## Verification

✅ **Before:** 4 occurrences of "51/2021"  
✅ **After:** 3 occurrences of "51/2021"  
✅ Duplicate link removed  
✅ Correct PDF link preserved  
✅ File deployed to production

## Result

The history page now has only ONE link for "View Advt No. 51/2021 (RGU)" pointing to the correct local PDF file.

## Live URL

🌐 https://prabhu.app/lateral-entry/pages/history.html

Scroll to "2021: Major Expansion" section to verify the change.

## Status

✅ **DUPLICATE REMOVED SUCCESSFULLY**

