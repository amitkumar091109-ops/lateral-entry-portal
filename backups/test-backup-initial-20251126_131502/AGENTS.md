<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->

# Lateral Entry Portal - Agent Guidelines

## Build/Run Commands
- **Run data manager**: `uv run python data/data_manager.py`
- **Run data collection**: `uv run python data/data_collection.py`
- **Initialize database**: `uv run python database/init_database.py`
- **Populate verified data**: `uv run python database/populate_verified_data.py`
- **Quick database update**: `uv run python database/quick_update.py`
- **Start API server**: `uv run --with flask --with flask-cors python api/server.py`
- **Export static JSON**: `./export_static_data.sh` (run after DB updates)
- **View portal locally**: `python3 -m http.server 8000` then open `http://localhost:8000/`
- **Production URL**: `https://prabhu.app/lateral-entry/`
- **No tests configured** - Add pytest if needed

## Code Style & Conventions
- **Python**: Follow PEP 8, use snake_case for functions/variables, PascalCase for classes
- **Imports**: Standard library → Third party → Local (grouped with blank lines, e.g., sqlite3, json, os → pandas, matplotlib → local modules)
- **Types**: Use type hints for function signatures where beneficial
- **Docstrings**: Use triple-quoted strings with clear descriptions for classes and complex functions
- **Paths**: Use absolute paths (`/home/ubuntu/projects/lateral-entry-portal/...`) for database and file references
- **Database**: Always use parameterized queries with `?` placeholders (e.g., `params=(batch_year,)`) to prevent SQL injection
- **Error handling**: Use try/except with specific exceptions, always close DB connections in finally blocks
- **Classes**: Constructor should accept db_path parameter with default value pointing to project database
- **SQL Queries**: Use multi-line triple-quoted strings for readability, include proper JOINs and GROUP BY clauses

## Project Structure
- `index.html` - Main web interface (vanilla JS, Tailwind CSS v3, Font Awesome icons)
- `pages/` - Subpages (profiles, analytics, history, batch details, etc.)
- `assets/js/main.js` - Main JavaScript with API client and static JSON fallback
- `assets/css/custom.css` - Custom styles
- `database/` - SQLite schema (lateral_entry.db), initialization, and data population scripts
- `data/` - Data management, collection, validation, and JSON export utilities
  - `entrants.json` - Static export of all appointees (for deployment)
  - `stats.json` - Static export of statistics (for deployment)
- `analytics/` - Generated PNG visualizations using matplotlib/seaborn
- `api/server.py` - Flask API server (optional for development)

## Deployment
- Portal uses **static JSON fallback** when API server is unavailable
- Deployed to prabhu.app at `/lateral-entry/` subdirectory
- After database updates, run `./export_static_data.sh` to regenerate JSON files
- Upload `data/entrants.json` and `data/stats.json` to deployment server
- See `DEPLOYMENT_GUIDE.md` for complete instructions

## Path Structure (IMPORTANT)
- From `index.html`: Use `./pages/filename.html`
- From `pages/*.html` to other pages: Use `./filename.html` (sibling pages)
- From `pages/*.html` to home: Use `../index.html`
- Base path detection handles subdirectory deployments (`/lateral-entry/`)
- **Never use** `pages/pages/` or stack directory paths
