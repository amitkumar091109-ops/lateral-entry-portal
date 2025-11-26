# Deployment Guide for Lateral Entry Officers Database

> **Important:** This is an information database, NOT an application portal.

## Quick Fix Applied - Static JSON Fallback

The portal now automatically falls back to static JSON files when the API server is unavailable. This fixes the "Failed to load profiles" error on prabhu.app.

## How It Works

1. **Development Mode** (localhost:8000 or local file):
   - Tries to connect to API at `http://localhost:5000/api`
   - If API is available, uses live data
   - If API fails, automatically switches to static JSON

2. **Production Mode** (prabhu.app):
   - Tries to connect to API at `https://prabhu.app/api`
   - When this fails (no API server), automatically loads static JSON files
   - Loads from `/lateral-entry/data/entrants.json` and `/lateral-entry/data/stats.json`

## Files to Deploy

When deploying to prabhu.app, ensure these files are uploaded:

```
lateral-entry/
├── index.html
├── pages/
│   ├── profiles.html
│   ├── analytics.html
│   ├── history.html
│   ├── batch-2019.html
│   ├── batch-2021.html
│   ├── batch-2022.html
│   ├── profile-detail.html
│   ├── citations.html
│   ├── faq.html
│   └── 2024-cancellation.html
├── assets/
│   ├── js/
│   │   └── main.js (✨ UPDATED with static fallback)
│   └── css/
│       └── custom.css
├── data/
│   ├── entrants.json (✨ NEW - 50 profiles)
│   └── stats.json (✨ NEW - portal statistics)
├── analytics/
│   ├── batch_distribution.png
│   ├── category_distribution.png
│   ├── ministry_distribution.png
│   └── state_distribution.png
└── manifest.json
```

## Updating Data

When you add new data to the database:

1. **Start the API server** (if not already running):
   ```bash
   cd /home/ubuntu/projects/lateral-entry-portal
   uv run --with flask --with flask-cors python api/server.py
   ```

2. **Export to JSON**:
   ```bash
   ./export_static_data.sh
   ```

3. **Deploy updated files** to prabhu.app:
   - Upload `data/entrants.json`
   - Upload `data/stats.json`
   - No need to redeploy other files unless you changed them

## Testing

### Test Locally
```bash
# Open in browser without API server running
python3 -m http.server 8000
# Open: http://localhost:8000/index.html
# Should load data from JSON files
```

### Test on prabhu.app
1. Upload all files to `/var/www/html/lateral-entry/`
2. Visit: https://prabhu.app/lateral-entry/
3. Check browser console - should see:
   - "API Error" (expected - no API server)
   - "Switching to static mode..."
   - "Static entrants data loaded: 50 records"
   - "Static stats data loaded"

## Troubleshooting

### Profiles still not loading?
1. Check browser console for errors
2. Verify JSON files exist: https://prabhu.app/lateral-entry/data/entrants.json
3. Check file permissions (should be readable by web server)
4. Clear browser cache

### Navigation still broken?
1. Check that all paths use `./pages/` or `../` correctly
2. See `FIX_PLAN.md` for path structure

### Need live API instead?
Set up reverse proxy in nginx/apache:
```nginx
location /api {
    proxy_pass http://localhost:5000/api;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

## What Was Fixed in This Session

### 1. Path Stacking Bug (CRITICAL)
- **Issue**: URLs like `pages/pages/pages/...` stacking infinitely
- **Cause**: `createEntrantCard()`, `createBatchCard()`, and search links using `pages/` instead of `./pages/`
- **Fixed**: 
  - `main.js:144` - Smart profile card links (detects current directory)
  - `main.js:103` - Search redirect uses `./pages/`
  - `main.js:173` - Batch cards use `./pages/`
  - `profiles.html:55-75` - Fixed button closing tags

### 2. Data Loading Failure
- **Issue**: "Failed to load profiles" on prabhu.app
- **Cause**: No API server at `https://prabhu.app/api`
- **Fixed**: Added static JSON fallback system
  - Exports data to `data/entrants.json` and `data/stats.json`
  - Automatically detects API failure and loads static files
  - Works seamlessly for users (no manual switching needed)

## Summary

✅ Navigation fixed - no more path stacking  
✅ Data loading fixed - uses static JSON as fallback  
✅ Deployment ready - just upload files to prabhu.app  
✅ Easy updates - run `export_static_data.sh` and deploy JSON files  

The portal now works perfectly on prabhu.app/lateral-entry/ without requiring an API server!
