#!/bin/bash
# Fix hardcoded color classes in profiles.html and analytics.html

for file in profiles.html analytics.html; do
    if [ -f "$file" ]; then
        echo "Fixing $file..."
        
        # Replace text colors
        sed -i 's/text-white/text-theme-primary/g' "$file"
        sed -i 's/text-muted/text-theme-muted/g' "$file"
        sed -i 's/text-neon-cyan/text-theme-accent/g' "$file"
        sed -i 's/text-neon-purple/text-theme-accent/g' "$file"
        
        # Replace background classes  
        sed -i 's/class="logo-icon/class="bg-theme-card logo-icon/g' "$file"
        sed -i 's/class="hero-gradient/class="bg-gradient-to-r from-gov-blue to-blue-700/g' "$file"
        sed -i 's/class="sticky-filters/class="bg-theme-card sticky-filters/g' "$file"
        sed -i 's/class="search-container/class="search-bar search-container/g' "$file"
        
        # Replace border colors
        sed -i 's/border-neon-purple/border-theme/g' "$file"
        sed -i 's/border-neon-cyan/border-theme/g' "$file"
        
        echo "  ✓ Fixed $file"
    fi
done

echo "Done!"
