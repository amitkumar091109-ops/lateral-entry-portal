#!/usr/bin/env python3
"""
Apply theme system to all HTML pages
"""

import os
import re
from pathlib import Path

# Pages to update (profiles.html and analytics.html already have themes)
pages_to_update = [
    "pages/history.html",
    "pages/faq.html",
    "pages/citations.html",
    "pages/batch-2019.html",
    "pages/batch-2021.html",
    "pages/batch-2023.html",
    "pages/profile-detail.html",
    "pages/2024-cancellation.html",
]

# CSS replacements (from old class to theme class)
replacements = [
    # Backgrounds
    (r"bg-gray-50(?![0-9])", "bg-theme-secondary"),
    (r"bg-white(?![a-z-])", "bg-theme-card"),
    (r"bg-gray-100(?![0-9])", "bg-theme-secondary"),
    # Text colors
    (r"text-gray-900(?![0-9])", "text-theme-primary"),
    (r"text-gray-800(?![0-9])", "text-theme-primary"),
    (r"text-gray-700(?![0-9])", "text-theme-secondary"),
    (r"text-gray-600(?![0-9])", "text-theme-secondary"),
    (r"text-gray-500(?![0-9])", "text-theme-muted"),
    (r"text-gray-400(?![0-9])", "text-theme-muted"),
    # Borders
    (r"border-gray-200(?![0-9])", "border-theme"),
    (r"border-gray-300(?![0-9])", "border-theme"),
]


def add_theme_css_link(content):
    """Add themes.css link if not present"""
    if "themes.css" in content:
        return content

    # Find custom.css and add themes.css after it
    pattern = r'(<link rel="stylesheet" href="../assets/css/custom\.css">)'
    replacement = r'\1\n    <link rel="stylesheet" href="../assets/css/themes.css">'
    content = re.sub(pattern, replacement, content)

    # If custom.css not found, try alternative patterns
    if "themes.css" not in content:
        pattern = r"(<link.*?custom\.css.*?>)"
        replacement = r'\1\n    <link rel="stylesheet" href="../assets/css/themes.css">'
        content = re.sub(pattern, replacement, content)

    return content


def add_theme_switcher_script(content):
    """Add theme-switcher.js script if not present"""
    if "theme-switcher.js" in content:
        return content

    # Find main.js and add theme-switcher.js before it
    pattern = r'(<script src="../assets/js/main\.js"></script>)'
    replacement = r'<script src="../assets/js/theme-switcher.js"></script>\n    \1'
    content = re.sub(pattern, replacement, content)

    # If main.js not found, add before closing body tag
    if "theme-switcher.js" not in content:
        pattern = r"(</body>)"
        replacement = r'    <script src="../assets/js/theme-switcher.js"></script>\n\1'
        content = re.sub(pattern, replacement, content)

    return content


def apply_theme_classes(content):
    """Replace standard Tailwind classes with theme classes"""
    for old_class, new_class in replacements:
        content = re.sub(old_class, new_class, content)
    return content


def process_file(filepath):
    """Process a single HTML file"""
    print(f"Processing {filepath}...")

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Apply transformations
        content = add_theme_css_link(content)
        content = add_theme_switcher_script(content)
        content = apply_theme_classes(content)

        # Only write if changes were made
        if content != original_content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  ✓ Updated {filepath}")
            return True
        else:
            print(f"  - No changes needed for {filepath}")
            return False

    except Exception as e:
        print(f"  ✗ Error processing {filepath}: {e}")
        return False


def main():
    """Main function"""
    project_root = Path(__file__).parent

    print("=" * 60)
    print("Applying Theme System to All Pages")
    print("=" * 60)
    print()

    updated_count = 0

    for page_path in pages_to_update:
        full_path = project_root / page_path
        if full_path.exists():
            if process_file(full_path):
                updated_count += 1
        else:
            print(f"  ✗ File not found: {page_path}")

    print()
    print("=" * 60)
    print(f"Summary: {updated_count}/{len(pages_to_update)} files updated")
    print("=" * 60)


if __name__ == "__main__":
    main()
