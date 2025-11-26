# Theme System Testing Guide

## Quick Test (5 minutes)

### 1. Access the Portal
Visit: **https://prabhu.app/lateral-entry/**

### 2. Locate Theme Switcher
Look for the **floating palette icon** (🎨) in the bottom-right corner of your screen.
- On mobile: Above the bottom navigation bar
- On desktop: Fixed to bottom-right corner

### 3. Test Each Theme

#### Regular Theme (Default - Government Blue)
- Click palette icon → Select "Regular"
- **Expected**: Clean blue interface, professional look
- **Check**: Headers should be blue, cards white, text dark gray

#### Vintage Theme (Classic Brown/Sepia)
- Click palette icon → Select "Vintage"
- **Expected**: Warm beige background, serif fonts (Georgia)
- **Check**: Should feel like reading a classic newspaper
- **Font Check**: Headings should be in serif font

#### Cyberpunk Theme (Neon Dark)
- Click palette icon → Select "Cyberpunk"
- **Expected**: Dark background, neon purple/cyan glows
- **Check**: Cards should have glassmorphism effect
- **Font Check**: Should load "Space Grotesk" font (modern sans-serif)
- **Animation Check**: Hover over cards for glow effects

#### Minimalist Theme (Clean Monochrome)
- Click palette icon → Select "Minimalist"
- **Expected**: Pure black & white, ultra-clean
- **Check**: No colors except black/gray/white
- **Font Check**: Very thin Inter font

### 4. Test Persistence
1. Select any theme (e.g., Cyberpunk)
2. **Refresh the page** (F5 or Ctrl+R)
3. **Expected**: Theme should remain Cyberpunk
4. Navigate to another page (e.g., Profiles)
5. **Expected**: Theme still Cyberpunk

### 5. Test Cross-Page Consistency
With theme set to Cyberpunk:
1. Visit Homepage → Should be dark with neon
2. Click "All Profiles" → Should stay dark with neon
3. Click "Analytics" → Should stay dark with neon
4. Click "History" → Should stay dark with neon

## Detailed Testing Checklist

### Functional Tests
- [ ] Theme switcher button appears
- [ ] Theme menu opens when clicked
- [ ] All 4 themes listed in menu
- [ ] Active theme highlighted in menu
- [ ] Clicking theme closes menu
- [ ] Clicking outside menu closes it
- [ ] ESC key closes menu
- [ ] Theme persists after page refresh
- [ ] Theme persists across page navigation

### Visual Tests per Theme

#### Regular Theme
- [ ] Blue header with white background
- [ ] Clean cards with subtle shadows
- [ ] Dark text on light background
- [ ] Batch cards have colored icons

#### Vintage Theme
- [ ] Beige/cream background
- [ ] Serif fonts load correctly
- [ ] Brown/amber color scheme
- [ ] Vintage newspaper aesthetic
- [ ] Drop shadows on cards

#### Cyberpunk Theme
- [ ] Dark gradient background
- [ ] Neon purple/cyan/pink accents
- [ ] Space Grotesk font loads
- [ ] Cards have glassmorphism blur
- [ ] Glowing borders on hover
- [ ] Neon batch badges

#### Minimalist Theme
- [ ] Pure white background
- [ ] Black text only
- [ ] Thin Inter font
- [ ] Minimal shadows
- [ ] Sharp, clean edges

### Browser Testing
- [ ] Chrome/Edge (Windows)
- [ ] Firefox (Windows)
- [ ] Safari (Mac/iOS)
- [ ] Chrome (Android)
- [ ] Mobile responsive (below 768px)

### Performance Tests
- [ ] Theme switch is instant (<100ms)
- [ ] No flash of unstyled content
- [ ] Fonts load within 1 second
- [ ] No console errors
- [ ] localStorage writes successfully

## Known Good Configurations

### Desktop
- **Chrome 120+**: ✅ All features working
- **Firefox 121+**: ✅ All features working
- **Safari 17+**: ✅ All features working
- **Edge 120+**: ✅ All features working

### Mobile
- **iOS Safari**: ✅ Theme button above bottom nav
- **Chrome Android**: ✅ Full functionality
- **Firefox Android**: ✅ Full functionality

## Troubleshooting

### Theme Switcher Not Appearing
1. Check browser console for errors (F12)
2. Verify `theme-switcher.js` loaded: DevTools → Network → JS
3. Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

### Fonts Not Loading
- **Cyberpunk theme**: Space Grotesk should load from Google Fonts
- **Minimalist theme**: Inter should load from Google Fonts
- Check Network tab for font requests
- May take 1-2 seconds on first load

### Theme Not Persisting
1. Check localStorage is enabled in browser
2. Open DevTools → Application → Local Storage
3. Look for key: `lateral-entry-theme`
4. Value should be: `regular`, `vintage`, `cyberpunk`, or `minimalist`

### Colors Look Wrong
1. Make sure you're testing on https://prabhu.app/lateral-entry/
2. Clear browser cache
3. Check `themes.css` is loaded (DevTools → Network → CSS)

## Report Issues

If you find bugs or issues:

1. **Note**: Theme name, browser, OS
2. **Screenshot**: Capture the issue
3. **Console**: Copy any error messages from F12 console
4. **Steps**: How to reproduce the issue

## Success Criteria

✅ All 4 themes switch smoothly  
✅ No visual glitches or broken layouts  
✅ Fonts load within 2 seconds  
✅ Theme persists across sessions  
✅ Mobile UI works without overlaps  
✅ No console errors  

---

**Happy Testing! 🎨**
