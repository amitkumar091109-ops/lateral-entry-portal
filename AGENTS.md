# Lateral Entry Portal - Agent Guidelines

## Build/Run Commands
- **Run data manager**: `uv run python data/data_manager.py`
- **Run data collection**: `uv run python data/data_collection.py`
- **Initialize database**: `uv run python database/init_database.py`
- **Populate verified data**: `uv run python database/populate_verified_data.py`
- **Quick database update**: `uv run python database/quick_update.py`
- **View portal**: Open `index.html` in browser
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
- `database/` - SQLite schema (lateral_entry.db), initialization, and data population scripts
- `data/` - Data management, collection, validation, and JSON export utilities
- `analytics/` - Generated PNG visualizations using matplotlib/seaborn (batch, ministry, state, category distributions)
