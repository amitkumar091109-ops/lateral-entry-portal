#!/bin/bash
# Quick verification script to test deployment

echo "=========================================="
echo "Lateral Entry Portal - Deployment Check"
echo "=========================================="
echo ""

# Test API endpoints
echo "1. Testing API Health..."
if curl -s https://prabhu.app/api/health | grep -q "healthy"; then
    echo "   ✅ API Health: PASS"
else
    echo "   ❌ API Health: FAIL"
fi

echo ""
echo "2. Testing API Stats..."
TOTAL=$(curl -s https://prabhu.app/api/stats | grep -o '"total_appointees": [0-9]*' | grep -o '[0-9]*')
if [ "$TOTAL" = "50" ]; then
    echo "   ✅ API Stats: PASS (50 appointees found)"
else
    echo "   ❌ API Stats: FAIL (Expected 50, got $TOTAL)"
fi

echo ""
echo "3. Testing Batch 2019..."
COUNT=$(curl -s https://prabhu.app/api/batches/2019 | grep -o '"count": [0-9]*' | head -1 | grep -o '[0-9]*')
if [ "$COUNT" = "8" ] || [ "$COUNT" = "9" ]; then
    echo "   ✅ Batch 2019: PASS ($COUNT appointees)"
else
    echo "   ❌ Batch 2019: FAIL (Expected 9, got $COUNT)"
fi

echo ""
echo "4. Testing Portal Homepage..."
if curl -s https://prabhu.app/lateral-entry/ | grep -q "India Lateral Entry Portal"; then
    echo "   ✅ Homepage: PASS"
else
    echo "   ❌ Homepage: FAIL"
fi

echo ""
echo "5. Testing Profiles Page..."
if curl -s https://prabhu.app/lateral-entry/pages/profiles.html | grep -q "All Appointees"; then
    echo "   ✅ Profiles Page: PASS"
else
    echo "   ❌ Profiles Page: FAIL"
fi

echo ""
echo "6. Testing Analytics Image..."
if curl -I https://prabhu.app/lateral-entry/analytics/batch_distribution.png 2>/dev/null | grep -q "image/png"; then
    echo "   ✅ Analytics Images: PASS"
else
    echo "   ❌ Analytics Images: FAIL"
fi

echo ""
echo "7. Checking API Server Status..."
if ps aux | grep -q "[p]ython.*server.py"; then
    echo "   ✅ API Server: RUNNING"
else
    echo "   ⚠️  API Server: NOT RUNNING"
    echo "      Start with: cd /home/ubuntu/projects/lateral-entry-portal && uv run --with flask --with flask-cors python api/server.py"
fi

echo ""
echo "8. Checking Nginx Status..."
if systemctl is-active --quiet nginx; then
    echo "   ✅ Nginx: RUNNING"
else
    echo "   ❌ Nginx: NOT RUNNING"
fi

echo ""
echo "=========================================="
echo "Deployment Check Complete!"
echo "=========================================="
echo ""
echo "Portal URL: https://prabhu.app/lateral-entry/"
echo "API URL:    https://prabhu.app/api/"
echo ""
echo "For manual browser testing:"
echo "1. Visit: https://prabhu.app/lateral-entry/"
echo "2. Check homepage shows '50' appointees"
echo "3. Click 'View All Profiles' - should load 50 cards"
echo "4. Click any batch - should show appointees"
echo "5. Open browser console (F12) - should see API success"
echo ""
