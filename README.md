# PantryPal
### An AI-Powered Kitchen Inventory & Recipe Assistant

PantryPal is a Python-based kitchen inventory application designed to help users track ingredients, reduce food waste, and discover recipes using ingredients they already have.

Built with Streamlit, SQLite, and the OpenAI API, PantryPal combines traditional inventory management with AI-powered recipe generation to create a practical, interactive kitchen assistant.

## Features

**Kitchen Inventory Management**
- Add, edit, and delete ingredients.
- Organize inventory by pantry, refrigerator, and freezer.
- Track quantities, units, categories, expiration dates, and notes.
- Search and filter ingredients by name and storage location.

**Expiration Tracking**
- Monitor ingredients approaching expiration.
- Prioritize ingredients that should be used soon.
- Highlight upcoming expiration dates on the dashboard.

**AI Recipe Generation**
- Generate three recipe suggestions based on current inventory.
- Prioritize ingredients approaching expiration.
- Customize serving sizes and the maximum number of additional ingredients.
- Clearly distinguish available ingredients from ingredients that need to be purchased.

**Excel Integration**
- Import multiple ingredients from Excel spreadsheets.
- Preview and validate spreadsheet data before importing.
- Identify duplicate entries and invalid rows.
- Export the current inventory to an Excel workbook.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | User interface |
| SQLite | Inventory database |
| OpenAI API | AI-powered recipe generation |
| Pandas | Data processing and Excel integration |
| OpenPyXL | Excel workbook creation and reading |
| python-dotenv | Environment variable management |

## Application Architecture

PantryPal uses a modular architecture:

- `app.py` — Streamlit interface and application workflows.
- `database.py` — SQLite database initialization and CRUD operations.
- `ai_recipes.py` — AI recipe generation and prompt construction.
- `data/pantry.db` — Local inventory database.

The application retrieves structured inventory records from SQLite, processes ingredient and expiration information, and passes relevant context to the OpenAI API to generate personalized recipe suggestions.

## Installation

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install the required dependencies.
4. Configure your OpenAI API key in a `.env` file.
5. Launch the Streamlit application.

Install dependencies:

```bash
pip install streamlit pandas openpyxl openai python-dotenv
```

Configure your `.env` file:

```text
OPENAI_API_KEY=your_api_key_here
```

Launch PantryPal:

```bash
python -m streamlit run app.py
```

## Future Improvements

Potential future enhancements include:
- AI-powered ingredient recognition from photos.
- Grocery receipt scanning.
- Voice-based inventory entry.
- Automated inventory notifications.
- Weekly meal planning.
- Automatic inventory adjustments when recipes are prepared.

## Project Motivation

PantryPal was developed as a hands-on project to explore practical AI integration, Python application development, database management, and data processing.

The goal was to build something useful while developing experience connecting multiple technologies into a cohesive application.