# Zepto Support Assistant

## Overview

This module implements a small offline RAG-based support assistant for Zepto policies.

The system uses:

- Sentence Transformers with `all-MiniLM-L6-v2` for local embeddings
- ChromaDB for vector storage and retrieval
- LangGraph for intent routing and workflow orchestration
- Pydantic for structured responses
- FastAPI for the `/ask` API
- `MOCK_LLM=1` as the default deterministic offline mode

No API key or paid service is required for the graded baseline.

## Architecture

```text
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
User Query
      |
      v
classify_intent
      |
      +----------------------+
      |                      |
      v                      v
policy_question        general_question
      |                      |
      v                      v
retrieve_and_answer     direct_answer
      |
      v
Pydantic JSON Response
      |
      v
FastAPI /ask
1. Ingestion

The eight Zepto policy documents are stored in:

docs/doc_01.txt through docs/doc_08.txt

main.py loads these documents and creates one chunk per document.

2. Embedding

The all-MiniLM-L6-v2 Sentence Transformers model converts each document chunk into an embedding.

The embeddings are stored in a persistent ChromaDB collection named:

zepto_policies

3. Retrieval

For policy questions, the retrieve_and_answer LangGraph node embeds the user query and retrieves the top 3 most similar documents using cosine similarity.

4. Generation

In the required default mode, MOCK_LLM is enabled.

For a policy question, the system returns:

Based on the retrieved context: ...

using the top retrieved document.

For a general question, the deterministic response is:

I can only answer questions about Zepto policies right now.

The optional real-LLM path can be selected with:

MOCK_LLM=0

The retrieval stage itself still uses local embeddings and ChromaDB.

LangGraph Nodes

The graph contains three nodes:

classify_intent
retrieve_and_answer
direct_answer

The classify_intent node uses the required keyword heuristic in mock mode.

Policy keywords include:

delivery
return
refund
membership
tracking
cancel
gift card
support hours

A conditional edge routes the query to either retrieve_and_answer or direct_answer.

Structured Prompt

The optional LLM prompt follows the:

Role → Context → Task → Format → Length

structure.

It also includes:

An explicit negative constraint
A few-shot example

Negative constraint:

Do not answer using information that is not present in the provided context.

Response Schema

The API response follows this Pydantic schema:

{
  "answer": "string",
  "sources": ["doc_01"],
  "confidence": 1.0
}

For general questions, sources is an empty list.

Installation

From the support_assistant directory:

pip install -r requirements.txt
Run the API

Run:

uvicorn main:app --reload

The API will be available locally at:

http://127.0.0.1:8000
Example API Calls
Example 1 — Policy question

Request:

{
  "query": "How much is delivery for an order below INR 149?"
}

Example response:

{
  "answer": "Based on the retrieved context: Zepto delivers grocery and household essentials...",
  "sources": ["doc_01"],
  "confidence": 1.0
}
Example 2 — General question

Request:

{
  "query": "What is the capital of India?"
}

Response:

{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1.0
}
Docker

Build the image:

docker build -t zepto-support-assistant .

Run:

docker run -p 7860:7860 zepto-support-assistant

The FastAPI service will then be available on port 7860.

MOCK_LLM

The graded baseline uses mock mode by default.

MOCK_LLM unset → mock mode
MOCK_LLM=1     → mock mode
MOCK_LLM=0     → optional real-LLM mode

Mock mode is deterministic and does not require an API key.


Commit message:

```text
Document support assistant architecture and usage
