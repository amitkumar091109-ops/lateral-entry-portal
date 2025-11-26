#!/bin/bash
# Quick deployment script for prabhu.app
# This creates a deployment package with all necessary files

DEPLOY_DIR="lateral-entry-deploy"
PROJECT_DIR="/home/ubuntu/projects/lateral-entry-portal"

echo "================================================"
echo "Creating Deployment Package"
echo "================================================"

# Clean up old deployment directory
if [ -d "$DEPLOY_DIR" ]; then
    echo "Removing old deployment directory..."
    rm -rf "$DEPLOY_DIR"
fi

# Create deployment structure
echo "Creating directory structure..."
mkdir -p "$DEPLOY_DIR/pages"
mkdir -p "$DEPLOY_DIR/assets/js"
mkdir -p "$DEPLOY_DIR/assets/css"
mkdir -p "$DEPLOY_DIR/data"
mkdir -p "$DEPLOY_DIR/analytics"

# Copy HTML files
echo "Copying HTML files..."
cp index.html "$DEPLOY_DIR/"
cp pages/*.html "$DEPLOY_DIR/pages/"

# Copy JavaScript and CSS
echo "Copying assets..."
cp assets/js/main.js "$DEPLOY_DIR/assets/js/"
cp assets/css/custom.css "$DEPLOY_DIR/assets/css/"

# Copy JSON data files
echo "Copying data files..."
cp data/entrants.json "$DEPLOY_DIR/data/"
cp data/stats.json "$DEPLOY_DIR/data/"
cp data/batches.json "$DEPLOY_DIR/data/"
cp data/batch-2019.json "$DEPLOY_DIR/data/"
cp data/batch-2021.json "$DEPLOY_DIR/data/"
cp data/batch-2022.json "$DEPLOY_DIR/data/"

# Copy analytics images
echo "Copying analytics images..."
cp analytics/*.png "$DEPLOY_DIR/analytics/" 2>/dev/null || echo "No analytics images found"

# Copy manifest
cp manifest.json "$DEPLOY_DIR/" 2>/dev/null || echo "No manifest.json found"

# Count files
FILE_COUNT=$(find "$DEPLOY_DIR" -type f | wc -l)

echo ""
echo "================================================"
echo "Deployment Package Ready!"
echo "================================================"
echo "Location: $PROJECT_DIR/$DEPLOY_DIR/"
echo "Total files: $FILE_COUNT"
echo ""
echo "Directory structure:"
tree -L 2 "$DEPLOY_DIR" 2>/dev/null || find "$DEPLOY_DIR" -type d | sed 's|[^/]*/| |g'
echo ""
echo "================================================"
echo "Next Steps:"
echo "================================================"
echo "1. Upload contents of '$DEPLOY_DIR/' to:"
echo "   /var/www/html/lateral-entry/"
echo ""
echo "2. Or create a tarball:"
echo "   tar -czf lateral-entry-$(date +%Y%m%d).tar.gz $DEPLOY_DIR/"
echo ""
echo "3. Or rsync to server:"
echo "   rsync -avz $DEPLOY_DIR/ user@prabhu.app:/var/www/html/lateral-entry/"
echo "================================================"
