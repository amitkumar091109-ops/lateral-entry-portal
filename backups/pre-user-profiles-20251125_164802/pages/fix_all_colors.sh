#!/bin/bash
# Replace all hardcoded gov-blue colors with theme-aware classes

echo "Fixing hardcoded colors in all pages..."

for file in *.html; do
    if [ -f "$file" ]; then
        echo "Processing $file..."
        
        # Replace text colors
        sed -i 's/text-gov-blue/text-theme-accent/g' "$file"
        
        # Replace background colors
        sed -i 's/bg-gov-blue/bg-gradient-to-r from-gov-blue to-blue-700/g' "$file"
        
        # Replace border colors
        sed -i 's/border-gov-blue/border-theme-accent/g' "$file"
        
        # Fix specific icon colors that should use primary
        sed -i 's/fas fa-\([a-z-]*\) text-theme-accent mr-/fas fa-\1 text-theme-accent mr-/g' "$file"
        
        echo "  ✓ Fixed $file"
    fi
done

echo ""
echo "All pages fixed!"
