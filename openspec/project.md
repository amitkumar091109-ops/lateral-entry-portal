# Project Context

## Purpose
The Lateral Entry Portal is a comprehensive web platform that showcases lateral entry appointees to the Government of India. It provides detailed profiles, statistics, and analytics about professionals who have joined civil services through lateral entry across three batches (2019, 2021, 2023).

## Tech Stack

### Current Stack
- **Frontend**: Vanilla HTML5, JavaScript ES6, Tailwind CSS v3, Font Awesome icons
- **Backend/Data**: Python 3.13, SQLite, Flask API (optional)
- **Data Processing**: Pandas, Matplotlib, Seaborn for analytics
- **Deployment**: Static files with JSON fallback, deployed at prabhu.app/lateral-entry/

### Dependencies
- Tailwind CSS: CDN-based, v3
- Font Awesome: v6.4.0
- Google Fonts: Inter font family
- Python packages: Flask, Flask-CORS, pandas, matplotlib, seaborn

## Project Conventions

### Code Style
- **Python**: PEP 8, snake_case for functions/variables, PascalCase for classes
- **JavaScript**: ES6+, camelCase for variables and functions
- **HTML**: Semantic HTML5 with accessibility attributes
- **CSS**: Utility-first Tailwind, custom CSS variables for theming
- **Naming**: Descriptive names, avoid abbreviations unless widely known

### File Structure
- `index.html` - Main landing page
- `pages/` - Subpages (profiles, analytics, history, batch details)
- `assets/js/` - JavaScript modules
- `assets/css/` - Custom CSS and themes
- `data/` - Static JSON exports and data management scripts
- `database/` - SQLite database and schema
- `analytics/` - Generated visualizations

### Path Conventions
- From `index.html`: Use `./pages/filename.html`
- Between pages: Use `./filename.html` (sibling pages)
- From pages to home: Use `../index.html`
- Base path detection handles subdirectory deployments

### Architecture Patterns
- **Static-first**: Portal works without backend via JSON fallback
- **Progressive Enhancement**: API server optional for development
- **Mobile-first**: Responsive design optimized for all devices
- **Theme System**: Multi-theme support with CSS custom properties
- **Component Pattern**: Reusable JavaScript functions in main.js

### Testing Strategy
- **Manual testing**: Visual testing across devices and browsers
- **No automated tests**: Currently no test framework configured
- **Future**: Add pytest for Python, Jest/Vitest for JavaScript

### Git Workflow
- Direct commits to main branch
- Descriptive commit messages focused on "why" not "what"
- Backup snapshots before major changes (see backups/ folder)

## Domain Context

### Lateral Entry Programme
Lateral entry refers to the appointment of specialists from the private sector to senior government positions (Joint Secretary, Director, Deputy Secretary levels). The programme aims to bring domain expertise and fresh perspectives to public administration.

### Data Sources
- **Government**: UPSC announcements, ministry press releases, DoPT notifications
- **Media**: Times of India, Economic Times, The Hindu, Business Standard
- **Professional**: LinkedIn profiles, official biographies, conference profiles

### Key Entities
- **Batches**: 2019 (Ad No. 17/2018), 2021 (Ad No. 47/2020), 2023 (Ad No. 52 & 53/2023)
- **Positions**: Joint Secretary (JS), Director, Deputy Secretary (DS)
- **Ministries**: Finance, Technology, Healthcare, Education, etc.
- **Categories**: Professional expertise areas (Finance, Technology, Public Policy, etc.)

## Important Constraints

### Technical Constraints
- Must work without backend (static JSON fallback required)
- CDN-based dependencies (no npm/build step in production)
- Subdirectory deployment at `/lateral-entry/` on prabhu.app
- Mobile-first with touch-friendly interfaces
- Performance: Fast loading on mobile networks

### Business Constraints
- Public transparency portal (no authentication required)
- Data sourced from public records only
- Must maintain data accuracy and citation
- Accessibility compliance (WCAG 2.1 AA target)

### Data Constraints
- SQLite database as primary storage
- JSON exports for static deployment
- Parameterized SQL queries (prevent injection)
- Quality scoring system (0-100) for profiles
- Cross-reference multiple sources for verification

## External Dependencies

### CDN Services
- Tailwind CSS: `https://cdn.tailwindcss.com`
- Google Fonts: `https://fonts.googleapis.com`
- Font Awesome: `https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/`

### Optional Services
- Flask API server (development only): `localhost:5000/api` or `/lateral-entry/api`
- Nginx proxy for API in production (when enabled)

### Data Collection
- Web scraping utilities (BeautifulSoup) for future expansion
- Manual data entry and verification
- Government portal monitoring for updates

## Current Limitations

### UI/UX Issues
- Vanilla JavaScript can be verbose for complex interactions
- Limited state management (no framework)
- Theme switching implemented but could be enhanced
- Search and filter logic scattered across pages
- Inconsistent component patterns

### Performance
- No code splitting or lazy loading
- All JavaScript loaded upfront
- Large JSON files loaded in memory
- No service worker or caching strategy

### Maintainability
- Duplicate code across page files
- Inline JavaScript in HTML files
- No component reusability
- Manual theme class management
- Limited error handling

### Future Needs
- Better state management
- Component-based architecture
- Build tooling for optimization
- Advanced search and filtering
- Real-time data updates
- User preferences and personalization
