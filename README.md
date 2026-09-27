# Zepto AI/ML Capstone

An end-to-end AI/ML engineering capstone containing three connected modules:

1. Data Pipeline
2. Analytics
3. GenAI Support Assistant

## Project Structure

- `/data_pipeline` - Web scraping, cleaning, currency conversion, SQLite storage, and SQL/pandas analysis.
- `/analytics` - Dataset profiling, preprocessing, machine learning, and evaluation.
- `/support_assistant` - Grounded GenAI support assistant using Zepto policy documents.

## Modules

### Data Pipeline

Scrapes product data from Books to Scrape, cleans the data, converts GBP prices to INR using the fixed rate of 1 GBP = 105.50 INR, stores the data in normalized SQLite tables, and performs SQL and pandas analysis.

The module includes SQL queries using SELECT, WHERE, ORDER BY, LIMIT, DISTINCT, IN, BETWEEN, and JOIN. It also compares SQL JOIN results with pandas `merge()` results.

### Analytics

Loads and analyzes the Titanic dataset, performs missing-value handling, visualization, standardization, survival analysis, classification, imbalance handling, Random Forest hyperparameter tuning, regression, and model evaluation.

The module contains:

- `01_eda.ipynb`
- `02_modelling.ipynb`
- `titanic.csv`
- `best_pipeline.joblib`

### GenAI Support Assistant

Builds a Zepto policy support assistant using eight policy documents, local Sentence Transformer embeddings, ChromaDB retrieval, LangGraph routing, Pydantic validation, and FastAPI.

The required baseline uses deterministic mock mode and does not require an LLM API key.

## Requirements

Python 3.10 or later is recommended.

The Support Assistant dependencies are listed in:

```text
support_assistant/requirements.txt
The Support Assistant uses:

FastAPI
Uvicorn
Pydantic
ChromaDB
Sentence Transformers
LangGraph

The Data Pipeline and Analytics modules use the Python libraries required by their notebooks and scripts.

Running the Project
1. Data Pipeline

Open the project and enter:

cd data_pipeline

Run:

python scrape_pipeline.py

Then create the SQLite database:

python database.py

Run the SQL and pandas analysis:

python sql_queries.py

The pipeline uses the fixed conversion rate:

1 GBP = 105.50 INR
2. Analytics

Open:

analytics/01_eda.ipynb

Run the notebook first.

Then open:

analytics/02_modelling.ipynb

and run it after the EDA notebook.

The committed titanic.csv provides an offline copy of the dataset for reproducibility.

The trained complete pipeline is saved as:

analytics/best_pipeline.joblib
3. Support Assistant

Enter the Support Assistant directory:

cd support_assistant

Install dependencies:

pip install -r requirements.txt

Run the FastAPI application:

uvicorn main:app --reload

The API provides:

POST /ask

Example request:

{
  "query": "What are the delivery charges?"
}

The required baseline uses mock mode. MOCK_LLM can be left unset or set to:

MOCK_LLM=1

Policy documents are stored in:

support_assistant/docs/

The Support Assistant uses local all-MiniLM-L6-v2 embeddings and ChromaDB for retrieval.

Support Assistant Architecture
Policy Documents
       |
       v
Document Ingestion
       |
       v
all-MiniLM-L6-v2 Embeddings
       |
       v
ChromaDB
       |
       v
LangGraph Intent Classification
       |
       +----------------------+
       |                      |
       v                      v
Policy Question        General Question
       |                      |
       v                      v
Retrieve Top-3          Direct Answer
       |
       v
Mock Answer Generation
       |
       v
Pydantic Response
       |
       v
FastAPI /ask

The three LangGraph nodes are:

classify_intent
retrieve_and_answer
direct_answer

The mock intent classifier uses policy keywords such as delivery, return, refund, membership, tracking, cancel, gift card, and support hours.

Docker

The Support Assistant includes a Dockerfile.

From the support_assistant directory:

docker build -t zepto-support-assistant .

Run:

docker run -p 7860:7860 zepto-support-assistant

The FastAPI service will be available on port 7860.

Design Decisions
One GitHub repository contains all three project modules.
The Data Pipeline uses the fixed GBP-to-INR rate of 105.50 for reproducible results without an external currency API.
SQLite provides normalized relational storage for the scraped data.
The Analytics module uses a committed titanic.csv as an offline dataset fallback.
The Analytics module saves the complete preprocessing and model pipeline as a single joblib artifact.
The Support Assistant uses local embeddings and ChromaDB so the required mock baseline does not require an LLM API key.
LangGraph provides conditional routing between policy retrieval and general-question handling.
FastAPI provides the Support Assistant API.
Docker provides a reproducible local container configuration.