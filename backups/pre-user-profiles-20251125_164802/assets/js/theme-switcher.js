/**
 * Lateral Entry Portal - Theme Switcher Module
 * Handles theme switching and persistence across all pages
 */

class ThemeSwitcher {
    constructor() {
        this.themes = ['regular', 'vintage', 'cyberpunk', 'minimalist'];
        this.currentTheme = this.getStoredTheme() || 'regular';
        this.init();
    }

    init() {
        // Apply stored theme on page load
        this.applyTheme(this.currentTheme);
        
        // Create theme switcher UI
        this.createThemeSwitcher();
        
        // Add event listeners
        this.attachEventListeners();
    }

    getStoredTheme() {
        try {
            return localStorage.getItem('lateral-entry-theme');
        } catch (e) {
            console.warn('localStorage not available:', e);
            return null;
        }
    }

    setStoredTheme(theme) {
        try {
            localStorage.setItem('lateral-entry-theme', theme);
        } catch (e) {
            console.warn('Could not save theme to localStorage:', e);
        }
    }

    applyTheme(theme) {
        if (!this.themes.includes(theme)) {
            theme = 'regular';
        }
        
        document.documentElement.setAttribute('data-theme', theme);
        this.currentTheme = theme;
        this.setStoredTheme(theme);
        
        // Update active state in menu if it exists
        this.updateActiveState();
        
        // Load theme-specific fonts
        this.loadThemeFonts(theme);
    }

    loadThemeFonts(theme) {
        // Remove existing theme font links
        const existingLinks = document.querySelectorAll('link[data-theme-font]');
        existingLinks.forEach(link => link.remove());

        // Load theme-specific fonts
        if (theme === 'cyberpunk') {
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = 'https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&display=swap';
            link.setAttribute('data-theme-font', 'true');
            document.head.appendChild(link);
        } else if (theme === 'minimalist') {
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap';
            link.setAttribute('data-theme-font', 'true');
            document.head.appendChild(link);
        }
        // Vintage uses Georgia (system font)
        // Regular uses default Tailwind fonts
    }

    createThemeSwitcher() {
        // Check if already exists
        if (document.querySelector('.theme-selector')) {
            return;
        }

        const html = `
            <div class="theme-selector">
                <button class="theme-btn" id="themeToggle" aria-label="Change theme">
                    <i class="fas fa-palette text-xl text-theme-primary"></i>
                </button>
                <div class="theme-menu" id="themeMenu">
                    <div class="theme-option" data-theme="regular">
                        <div class="theme-icon regular"></div>
                        <span class="text-sm font-medium">Regular</span>
                    </div>
                    <div class="theme-option" data-theme="vintage">
                        <div class="theme-icon vintage"></div>
                        <span class="text-sm font-medium">Vintage</span>
                    </div>
                    <div class="theme-option" data-theme="cyberpunk">
                        <div class="theme-icon cyberpunk"></div>
                        <span class="text-sm font-medium">Cyberpunk</span>
                    </div>
                    <div class="theme-option" data-theme="minimalist">
                        <div class="theme-icon minimalist"></div>
                        <span class="text-sm font-medium">Minimalist</span>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', html);
        this.updateActiveState();
    }

    attachEventListeners() {
        // Toggle menu
        document.addEventListener('click', (e) => {
            const themeToggle = document.getElementById('themeToggle');
            const themeMenu = document.getElementById('themeMenu');
            
            if (!themeToggle || !themeMenu) return;

            if (e.target.closest('#themeToggle')) {
                e.preventDefault();
                e.stopPropagation();
                themeMenu.classList.toggle('show');
            } else if (!e.target.closest('.theme-menu')) {
                themeMenu.classList.remove('show');
            }
        });

        // Theme selection
        document.addEventListener('click', (e) => {
            const themeOption = e.target.closest('.theme-option');
            if (themeOption) {
                const theme = themeOption.getAttribute('data-theme');
                this.applyTheme(theme);
                
                // Close menu
                const themeMenu = document.getElementById('themeMenu');
                if (themeMenu) {
                    themeMenu.classList.remove('show');
                }
            }
        });

        // Keyboard accessibility
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                const themeMenu = document.getElementById('themeMenu');
                if (themeMenu) {
                    themeMenu.classList.remove('show');
                }
            }
        });
    }

    updateActiveState() {
        const options = document.querySelectorAll('.theme-option');
        options.forEach(option => {
            if (option.getAttribute('data-theme') === this.currentTheme) {
                option.classList.add('active');
            } else {
                option.classList.remove('active');
            }
        });
    }

    // Public method to switch theme programmatically
    switchTo(theme) {
        this.applyTheme(theme);
    }

    // Public method to get current theme
    getCurrent() {
        return this.currentTheme;
    }
}

// Initialize theme switcher when DOM is ready
if (typeof window !== 'undefined') {
    let themeSwitcher;
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            themeSwitcher = new ThemeSwitcher();
            window.themeSwitcher = themeSwitcher;
        });
    } else {
        themeSwitcher = new ThemeSwitcher();
        window.themeSwitcher = themeSwitcher;
    }
}
