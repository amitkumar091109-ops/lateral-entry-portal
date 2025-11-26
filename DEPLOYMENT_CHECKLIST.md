# Quick Deployment Checklist

## ✅ Files Ready to Deploy

All fixes have been tested. Deploy these files to `prabhu.app/lateral-entry/`:

### Core HTML Files (11 files)
- [ ] `index.html`
- [ ] `pages/profiles.html`
- [ ] `pages/analytics.html`
- [ ] `pages/history.html`
- [ ] `pages/batch-2019.html`
- [ ] `pages/batch-2021.html`
- [ ] `pages/batch-2022.html`
- [ ] `pages/profile-detail.html`
- [ ] `pages/citations.html`
- [ ] `pages/faq.html`
- [ ] `pages/2024-cancellation.html`

### JavaScript & CSS (2 files)
- [ ] `assets/js/main.js` - API calls only (no static JSON fallback)
- [ ] `assets/css/custom.css`

### Database & API
- [✅] `api/server.py` - Flask API server
- [✅] `database/lateral_entry.db` - SQLite database with 45 appointees
- [❌] `data/` directory - REMOVED (all static JSON files deleted)

### Images & Assets
- [ ] `analytics/batch_distribution.png`
- [ ] `analytics/category_distribution.png`
- [ ] `analytics/ministry_distribution.png`
- [ ] `analytics/state_distribution.png`
- [ ] `manifest.json`

## 🧪 Testing After Deployment

### 1. Homepage Test (index.html)
Visit: `https://prabhu.app/lateral-entry/`
- [ ] See "50" total appointees (not --)
- [ ] See "20+" ministries
- [ ] See "3" batches
- [ ] Recent profiles load (6 cards)
- [ ] Search box works
- [ ] Batch cards clickable (2019, 2021, 2022)

### 2. Profiles Page Test
Visit: `https://prabhu.app/lateral-entry/pages/profiles.html`
- [ ] All 50 profiles load
- [ ] Filter by batch works (2019: 9, 2021: 31, 2022: 10)
- [ ] Filter by position works (JS, Director, Deputy)
- [ ] Search by name works
- [ ] Click profile card goes to detail page (not stacking paths)

### 3. Batch Pages Test
Visit each:
- [ ] `https://prabhu.app/lateral-entry/pages/batch-2019.html` (9 appointees)
- [ ] `https://prabhu.app/lateral-entry/pages/batch-2021.html` (31 appointees)
- [ ] `https://prabhu.app/lateral-entry/pages/batch-2022.html` (10 appointees)

Check:
- [ ] Correct count displayed
- [ ] Stats cards show (Total, Ministries, Positions, Year)
- [ ] All appointee cards load
- [ ] "Explore Other Batches" links work

### 4. Mobile Navigation Test
On mobile or narrow browser:
- [ ] Bottom nav appears
- [ ] Home button works from any page
- [ ] Profiles button works
- [ ] Analytics button works
- [ ] History button works
- [ ] No path stacking (check URL bar)

### 5. Console Check
Open browser console (F12):
- [ ] See: "Switching to static mode..."
- [ ] See: "Static entrants data loaded: 50 records"
- [ ] See: "Static stats data loaded"
- [ ] See: "Static batch XXXX data loaded: X entrants" (when on batch pages)
- [ ] No JavaScript errors
- [ ] No 404 errors for JSON files

### 6. Path Verification
Click around and check URL bar:
- [ ] Homepage links: `/lateral-entry/pages/profiles.html` ✅
- [ ] Profiles to detail: `/lateral-entry/pages/profile-detail.html?id=X` ✅
- [ ] NOT: `/lateral-entry/pages/pages/...` ❌
- [ ] Back to home from subpage: `/lateral-entry/index.html` ✅

## 🚨 If Issues Occur

### Profiles/Batches not loading
1. Check console for errors
2. Verify JSON files uploaded: `https://prabhu.app/lateral-entry/data/entrants.json`
3. Check file permissions (chmod 644 for JSON files)
4. Hard refresh browser (Ctrl+Shift+R)

### Path stacking still happening
1. Verify `assets/js/main.js` was uploaded with latest changes
2. Clear browser cache
3. Check date modified on server matches local file

### Stats show dashes instead of numbers
1. Check `data/stats.json` exists and is readable
2. Open browser console for errors
3. Verify `main.js` has static fallback code

## 📊 What Changed Since Last Deployment

### Bugs Fixed:
1. ✅ Path stacking bug (`pages/pages/pages/...`)
2. ✅ Profile loading failure
3. ✅ Batch data loading failure

### Files Modified:
1. `assets/js/main.js` - Major update with static JSON fallback
2. `pages/profiles.html` - Fixed button closing tags

### Files Added:
1. `data/entrants.json` - All 50 appointees
2. `data/stats.json` - Portal statistics
3. `data/batches.json` - Batch summary
4. `data/batch-2019.json` - 2019 batch details
5. `data/batch-2021.json` - 2021 batch details
6. `data/batch-2022.json` - 2022 batch details

## ✨ Expected Result

After deployment, the portal should:
- ✅ Work perfectly on prabhu.app/lateral-entry/ without API server
- ✅ Load all data from static JSON files
- ✅ Navigate correctly without path stacking
- ✅ Display all 50 profiles across 3 batches
- ✅ Work on both desktop and mobile
- ✅ Have zero JavaScript errors

## 🔄 Future Data Updates

When database changes:
```bash
cd /home/ubuntu/projects/lateral-entry-portal
./export_static_data.sh
# Upload only the 6 JSON files to prabhu.app
```

---
**Last Updated**: Nov 24, 2025  
**Ready for Deployment**: ✅ YES
