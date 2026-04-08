# Food Recipe Recommender
 
A fullstack recipe recommendation platform with an async FastAPI backend, PostgreSQL database, Apache Airflow data pipeline, and AI-powered recommendations. Users can browse recipes from external APIs, add their own, log cooking attempts with notes, and receive intelligent recipe suggestions.
 
## Tech Stack
 
| Layer | Technology |
|-------|-----------|
| Backend API | FastAPI (Python 3.11), Pydantic, SQLAlchemy |
| Database | PostgreSQL via Neon (cloud) with pgvector |
| Data Pipeline | Apache Airflow (Dockerized) |
| AI / Embeddings | sentence-transformers (planned) |
| Frontend | React with PWA support (in progress) |
| External Data | TheMealDB API |
 
## Features
 
**Implemented**
- Full CRUD operations for recipes and cooking logs
- External recipe ingestion from TheMealDB with ETL transformation
- Duplicate detection on recipe imports
- Query parameter filtering by area and category
- Nested JSON responses with recipe-ingredient relationships
- Automated weekly data pipeline via Airflow DAG
- Pydantic schema validation on all endpoints
 
**Planned**
- AI-powered recipe recommendations using pgvector and sentence-transformers
- React frontend with mobile-friendly PWA
- JWT authentication and user profiles
- Shopping list generation with share-to-phone export
- Voice-to-text recipe input
- Raspberry Pi self-hosted deployment
 
## API Endpoints
 
### Recipes
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/recipes` | Get all recipes (filterable by `?area=` and `?category=`) |
| GET | `/recipes/{id}` | Get a single recipe with ingredients |
| POST | `/recipes` | Create a recipe with ingredients |
| PUT | `/recipes/{id}` | Update a recipe |
| DELETE | `/recipes/{id}` | Delete a recipe |
 
### Cooking Logs
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/cooking-logs` | Get all logs (filterable by `?recipe_id=`) |
| GET | `/cooking-logs/{id}` | Get a single cooking log |
| POST | `/cooking-logs` | Log a new cook with notes and rating |
| PUT | `/cooking-logs/{id}` | Update a cooking log |
| DELETE | `/cooking-logs/{id}` | Delete a cooking log |
 
### Data Ingestion
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/meals/search/{search_term}` | Fetch and store recipes from TheMealDB |
 
## Project Structure
 
```
food-recipe-recommender/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── config.py            # Pydantic settings (env variables)
│   │   ├── database.py          # Async engine, session, Base
│   │   ├── models/
│   │   │   └── recipe.py        # SQLAlchemy models (Recipe, Ingredient, CookingLog)
│   │   ├── routes/
│   │   │   ├── recipe.py        # Recipe CRUD endpoints
│   │   │   ├── cooking_log.py   # Cooking log endpoints
│   │   │   └── meal_db.py       # TheMealDB ingestion endpoint
│   │   ├── schemas/
│   │   │   ├── recipe.py        # Recipe/Ingredient Pydantic schemas
│   │   │   └── cooking_log.py   # CookingLog Pydantic schemas
│   │   └── services/
│   │       └── meal_db.py       # TheMealDB API client and transformer
│   ├── requirements.txt
│   └── .env
├── data-pipeline/               # Airflow DAGs (runs on separate machine via Docker)
├── frontend/                    # React app (in progress)
├── FEATURES.md                  # Future feature ideas
└── README.md
```
 
## Database Schema
 
```
recipe
├── id (PK)
├── name
├── instructions
├── link
├── author
├── area
├── category
└── source
 
ingredient
├── id (PK)
├── name
├── quantity
├── unit
└── recipe_id (FK → recipe.id)
 
cooking_log
├── id (PK)
├── date_cooked
├── notes
├── rating
└── recipe_id (FK → recipe.id)
```
 
## Data Pipeline
 
The Airflow DAG (`recipe_ingestion`) runs on a weekly schedule and performs:
 
1. **Extract** — Fetches all meal categories from TheMealDB, then retrieves full recipe details for every meal in each category
2. **Transform** — Reshapes TheMealDB's format (20 separate ingredient fields) into normalized recipe and ingredient dictionaries
3. **Load** — Inserts into PostgreSQL with duplicate checking by recipe name
 
## Getting Started
 
### Prerequisites
- Python 3.11
- PostgreSQL database (Neon recommended)
- Node.js 18+ (for frontend)
- Docker (for Airflow pipeline)
 
### Backend Setup
 
```bash
cd backend
py -3.11 -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```
 
Create a `.env` file in `backend/`:
```
DATABASE_URL=postgresql+asyncpg://user:password@host/dbname
```
 
Run the server:
```bash
uvicorn app.main:app --reload
```
 
API docs available at `http://localhost:8000/docs`
 
### Airflow Setup (requires Docker)
 
```bash
cd data-pipeline
docker compose up airflow-init
docker compose up -d
```
 
Airflow dashboard at `http://localhost:8080` (default: airflow/airflow)
 
## Author
 
Sanaa Otgonbayar — [GitHub](https://github.com/OSanaa) | [LinkedIn](https://linkedin.com/in/munkhsanaaotgonbayar)
