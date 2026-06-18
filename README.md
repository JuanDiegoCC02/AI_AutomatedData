# 📘 AI Automated Data

AI Automated Data is an AI-powered document processing and semantic search platform built with Django REST Framework, ChromaDB, and Sentence Transformers.

The system automatically extracts, analyzes, indexes, and retrieves information from uploaded documents using vector embeddings and semantic similarity search.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-6.0-green)
![Django REST Framework](https://img.shields.io/badge/DRF-API-red)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Database-orange)
![Sentence Transformers](https://img.shields.io/badge/SentenceTransformers-NLP-purple)

---

# 🚀 Overview

This project provides an end-to-end document intelligence pipeline capable of:

* Extracting text from PDF documents
* Cleaning and preprocessing text
* Detecting document language
* Measuring text complexity
* Generating semantic embeddings
* Performing semantic search
* Tracking processing quality metrics

The platform stores document vectors in ChromaDB and exposes a REST API for document management and retrieval.

---

# ⚙️ Tech Stack

* Django REST Framework
* ChromaDB
* Sentence Transformers
* LangDetect
* NumPy
* drf-spectacular (OpenAPI / Swagger)

---

# 🧠 Core Features

## Document Processing

* PDF text extraction
* Automatic text cleaning
* Language detection
* Complexity analysis
* Chunk generation for large documents

## Semantic Search

* Vector embeddings generation
* ChromaDB vector storage
* Similarity-based document retrieval
* Semantic document matching

## Analytics & Reporting

* Document quality scoring
* Duplicate chunk detection
* Processing statistics
* Dashboard metrics
* Language distribution reports

## Document Management

* Upload documents
* List documents
* Delete documents
* Pagination support
* Filtering and ordering

---

# 📡 API Endpoints

### Documents

* POST `/api/upload/`
* GET `/api/documents/`
* DELETE `/api/delete-document/{id}/`

### Search

* POST `/api/search/`

### Analytics

* GET `/api/stats/`
* GET `/api/dashboard/`
* GET `/api/quality-report/`
* GET `/api/top-documents/`

---

# 📄 API Documentation

* Swagger UI: `/api/docs/`
* OpenAPI Schema: `/api/schema/`
* Redoc: `/api/redoc/`

---

# 🔍 Query Features

### Pagination

```http
GET /api/documents/?page=1&page_size=5
```

### Filtering

```http
GET /api/documents/?language=es
```

```http
GET /api/documents/?status=COMPLETED
```

### Ordering

```http
GET /api/documents/?ordering=-quality_score
```

```http
GET /api/documents/?ordering=-uploaded_at
```

---

# 🏗️ Project Structure

```text
data_pipeline/
├── services/
│   ├── cleaner.py
│   ├── chunker.py
│   ├── complexity_service.py
│   ├── embeddings.py
│   ├── extractor.py
│   ├── language_detector.py
│   ├── quality_service.py
│   ├── search_service.py
│   └── vector_store.py
│
├── filters.py
├── pagination.py
├── serializers.py
├── views.py
├── models.py
└── urls.py
```

---

# Credits

Juan Diego Corella Camacho

Backend Developer | Full Stack Developer | Telecommunications & Systems Engineering
