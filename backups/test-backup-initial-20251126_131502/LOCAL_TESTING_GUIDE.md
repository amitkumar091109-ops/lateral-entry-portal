# Lateral Entry Portal - Local Testing Guide

## Start the Portal

```bash
cd /home/ubuntu/projects/lateral-entry-portal/lateral-entry-deploy
python3 -m http.server 8000
```

Open browser: **http://localhost:8000/**

## ✅ Verification Checklist

### Homepage
- [ ] Shows **72 Total Appointees**
- [ ] **3 Batch Cards** (2019: 9, 2021: 36, 2023: 27)
- [ ] Recent appointments load (6 profiles)
- [ ] No console errors

### 2023 Batch Page
Navigate: `http://localhost:8000/pages/batch-2023.html`
- [ ] Header shows **27 appointees**
- [ ] All 27 profile cards display
- [ ] Statistics cards populate
- [ ] Sector list shows correctly

### Profiles Page
Navigate: `http://localhost:8000/pages/profiles.html`
- [ ] Shows **72 verified profiles**
- [ ] **2023 batch filter** button visible
- [ ] Clicking 2023 shows only 27 profiles
- [ ] All filters work (All, 2019, 2021, 2023)

## Browser Console Tests

Press **F12** → Console tab, run:

```javascript
// Test API
window.LateralEntry.API.stats().then(d => console.log('✅ Stats:', d.total_appointees));
window.LateralEntry.API.entrants().then(d => console.log('✅ Entrants:', d.length));
window.LateralEntry.API.batch(2023).then(d => console.log('✅ Batch 2023:', d.entrants.length));
```

Expected output:
```
✅ Stats: 72
✅ Entrants: 72
✅ Batch 2023: 27
```

## Deployment

When local tests pass, upload to: `https://prabhu.app/lateral-entry/`

See `2023_BATCH_COMPLETION_REPORT.md` for full details.
