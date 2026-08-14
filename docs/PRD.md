# Know Your Dharma

**Product Requirements Document (PRD)**  
**Version:** 1.0  
**Status:** Draft / Foundation  
**Product Type:** Enterprise-grade AI-powered Scripture Intelligence Platform  
**Initial Domain:** Sanatan Dharma  
**Primary Languages:** Sanskrit, Hindi, English

---

## 1. Product Vision

**Know Your Dharma** is an AI-powered Scripture Intelligence Platform designed to help users explore, search, understand, and study authentic Sanatan Dharma scriptures using modern AI technologies.

The platform will combine:

- Digitization of scanned scripture documents
- Sanskrit and Hindi OCR
- Structured scripture extraction
- Multilingual semantic search
- Hybrid RAG
- Local LLM-based response generation
- Citation-backed answers
- Scripture/page-level evidence
- Agentic workflows
- Secure user accounts
- Enterprise-grade storage, monitoring, evaluation, and administration

The primary objective is **not to create an AI that claims to know the scriptures**, but to create an AI system that can **retrieve authoritative source material and explain it to the user while clearly showing the underlying evidence**.

---

# 2. Problem Statement

A significant amount of authentic Hindu/Sanatan Dharma literature is available as scanned PDFs rather than machine-readable digital text.

These documents may contain:

- Sanskrit verses
- Hindi translations
- Sanskrit/Hindi commentary
- Chapter and verse numbering
- Footnotes
- Multiple columns
- Page headers and footers
- Complex layouts
- Scanned images

Traditional PDF text extraction frequently fails on these documents.

This creates several problems:

1. Scripture cannot be reliably searched.
2. Conventional RAG systems cannot directly consume scanned pages.
3. OCR may introduce Sanskrit/Hindi errors.
4. Verse structure can be lost during extraction.
5. AI-generated answers may lack reliable citations.
6. Users cannot easily verify an AI response against the original source.
7. Large scripture collections are difficult to navigate manually.

Know Your Dharma will address these problems through an end-to-end document intelligence and RAG platform.

---

# 3. Product Goals

## 3.1 Primary Goals

### G1 — Digitize Scripture

Convert scanned and digital scripture PDFs into structured, searchable data.

### G2 — Sanskrit/Hindi OCR

Provide reliable OCR for Sanskrit and Hindi scripture content, including scanned pages.

### G3 — Structured Knowledge Base

Transform OCR output into structured entities such as:

- Scripture
- Volume
- Parva/Kanda
- Chapter
- Verse
- Sanskrit text
- Hindi translation
- Commentary
- Page
- Edition
- Publisher

### G4 — Multilingual Search

Allow users to search using:

- Sanskrit
- Hindi
- English
- Transliteration where supported

### G5 — Grounded AI Answers

Generate answers using retrieved scripture evidence rather than relying solely on the model's internal knowledge.

### G6 — Citation and Evidence

Every significant answer should provide source references such as:

- Scripture
- Volume
- Chapter
- Verse
- Page
- Edition/Publisher
- Original scanned page where available

### G7 — Local LLM

Use a locally hosted LLM for final response generation during development and initial deployment.

The model runtime must remain abstracted so that the system can later support larger models or GPU servers.

### G8 — Enterprise Architecture

Support:

- Authentication
- Authorization
- User management
- Persistent storage
- Caching
- Audit logging
- Observability
- Evaluation
- Background processing
- Secure APIs
- Scalable deployment

---

# 4. Non-Goals for Initial Release

The following will not be part of the first production milestone:

- Full multi-religion support
- Mobile application
- Fine-tuning a foundation model
- Voice-first interaction
- Automatic Sanskrit pronunciation generation
- Complete knowledge graph implementation
- Autonomous religious interpretation
- Replacing qualified scholars or teachers

These may be considered in future releases.

---

# 5. Target Users

## 5.1 General Users

People who want to:

- Understand scripture
- Search for teachings
- Ask questions about concepts
- Find relevant verses

## 5.2 Students

Users studying:

- Bhagavad Gita
- Ramayana
- Mahabharata
- Upanishads
- Other scriptures

## 5.3 Researchers

Users who need:

- Source-level search
- Verse references
- Original Sanskrit
- Hindi translations
- Cross-scripture research

## 5.4 Content/Knowledge Managers

Users responsible for:

- Uploading documents
- Reviewing OCR
- Correcting extracted text
- Managing scripture metadata

## 5.5 Administrators

Users responsible for:

- User management
- Permissions
- System monitoring
- Document management
- Audit logs
- Evaluation
- Platform configuration

---

# 6. Initial Scripture Corpus

The initial corpus will focus on Sanatan Dharma.

Potential initial sources include:

- Bhagavad Gita
- Mahabharata
- Valmiki Ramayana
- Upanishads
- Selected Vedas
- Selected Puranas
- Other authoritative texts added later

The initial implementation will begin with available scanned scripture PDFs, including Gita Press material.

The platform must be designed so additional scriptures can be added without changing the core architecture.

---

# 7. Core Product Capabilities

## 7.1 Document Management

Administrators/content managers should be able to:

- Upload PDFs
- View document metadata
- Track processing status
- View document versions
- Retry failed processing
- Delete documents according to permissions
- View processing history

### Document states

```text
UPLOADED
↓
PROCESSING
↓
OCR_PROCESSING
↓
PARSING
↓
EMBEDDING
↓
INDEXING
↓
READY
```

Failure state:

```text
FAILED
```

---

# 8. OCR Requirements

The platform must support scanned documents.

### OCR pipeline

```text
PDF
 ↓
Page Extraction
 ↓
Image Preprocessing
 ↓
OCR
 ↓
Layout Detection
 ↓
Language Detection
 ↓
Text Segmentation
 ↓
Quality Validation
```

OCR should support:

- Sanskrit
- Hindi
- English where applicable

### OCR output should include

- Extracted text
- Page number
- Bounding boxes where available
- OCR confidence
- Detected language
- Processing metadata

### Low-confidence OCR

Pages or sections below a configured confidence threshold should be flagged for review rather than silently treated as authoritative.

---

# 9. Scripture Structure Extraction

OCR output should be transformed into structured scripture entities.

Example conceptual structure:

```text
Scripture
 └── Volume
      └── Parva/Kanda
           └── Chapter
                └── Verse
                     ├── Sanskrit
                     ├── Hindi Translation
                     └── Commentary
```

Each verse should have a unique identifier.

Example:

```text
BG-02-47
```

The exact identifier format may vary by scripture.

---

# 10. Multilingual Knowledge Representation

A verse should maintain relationships between different representations.

Example:

```text
Verse ID: BG-02-47

Sanskrit
    ↓
Hindi Translation
    ↓
English Translation
    ↓
Commentary
```

These should remain linked through the same canonical verse/entity.

The system should not treat each translation as an unrelated document.

---

# 11. Search Requirements

The search system should support:

### Exact Search

Useful for:

- Sanskrit phrases
- Verse numbers
- Names
- Specific terms

### Semantic Search

Useful for conceptual queries such as:

> What does the Gita say about attachment to the results of action?

### Hybrid Search

The target retrieval architecture is:

```text
User Query
    │
    ├── Dense Retrieval
    │
    └── BM25 / Lexical Retrieval
            │
            ▼
       Result Fusion
            │
            ▼
         Reranker
            │
            ▼
      Final Context
```

---

# 12. Vector Database Requirements

Qdrant will initially be used as the vector database.

Vectors may represent:

- Sanskrit
- Hindi
- English
- Commentary

Metadata should support filtering by:

- Scripture
- Volume
- Chapter
- Verse
- Language
- Publisher
- Edition
- Page

---

# 13. RAG Requirements

The RAG pipeline should follow:

```text
User Question
      ↓
Query Understanding
      ↓
Query Routing
      ↓
Hybrid Retrieval
      ↓
Reranking
      ↓
Context Selection
      ↓
Local LLM
      ↓
Citation Generation
      ↓
Citation Validation
      ↓
Final Answer
```

The system should prioritize retrieved source material over unsupported model knowledge.

If sufficient evidence cannot be retrieved, the system should clearly communicate that the available knowledge base does not contain enough information.

---

# 14. Local LLM Requirements

The initial response-generation system will use a locally hosted LLM.

Initial runtime:

```text
Ollama
```

The model should be selected based on:

- Sanskrit support
- Hindi support
- English support
- Reasoning capability
- Hardware constraints
- Quantized inference support

The application must use an abstraction layer:

```text
FastAPI
   ↓
LLM Service
   ↓
Model Provider Interface
   ↓
Ollama
```

This allows future migration to:

- vLLM
- larger local models
- GPU servers
- cloud inference

without redesigning the RAG system.

---

# 15. Response Generation Requirements

The response generator should:

1. Use retrieved context.
2. Avoid inventing scripture references.
3. Clearly distinguish source material from explanation.
4. Provide citations.
5. Prefer exact verse references where available.
6. Indicate insufficient evidence when necessary.
7. Preserve the meaning of the retrieved source.
8. Avoid presenting generated interpretations as direct scripture quotations.

---

# 16. Citation System

Citations are a core product feature, not an optional enhancement.

A citation should ideally contain:

```text
Scripture
Volume
Parva/Kanda
Chapter
Verse
Page
Edition
Publisher
```

Where available, users should be able to open the corresponding scanned page.

### Evidence viewer

```text
AI Answer
   │
   └── Citation
          │
          ├── Sanskrit
          ├── Hindi Translation
          ├── Commentary
          └── Original Page Image
```

---

# 17. Chat Application

The platform should provide a conversational interface.

Features:

- New conversation
- Continue conversation
- Streaming response
- Citation display
- Source preview
- Regenerate response
- Copy response
- User feedback
- Conversation history
- Delete conversation
- Bookmark useful verses

---

# 18. Authentication

The platform must support secure authentication.

Initial technology:

**Keycloak + OIDC/OAuth2**

Capabilities:

- User registration
- Login
- Logout
- Token management
- Role-based authorization
- Password management
- Future MFA
- Future enterprise identity providers

---

# 19. Authorization

The system should support RBAC.

Initial roles:

```text
SUPER_ADMIN
ADMIN
CONTENT_MANAGER
REVIEWER
USER
```

Permissions should determine:

- Document upload
- Document deletion
- OCR review
- User administration
- System administration
- Evaluation access
- Audit-log access

---

# 20. Database Requirements

PostgreSQL will be the primary relational database.

Core entities should include:

```text
Users
Organizations
Roles
Documents
DocumentVersions
Volumes
Chapters
Verses
Translations
Commentaries
OCRJobs
IngestionJobs
ChatSessions
Messages
Citations
Bookmarks
Feedback
AuditLogs
ModelUsage
EvaluationResults
```

PostgreSQL will be the **system of record**.

Qdrant will be used for vector retrieval, not as the primary application database.

---

# 21. Object Storage

Original and generated document artifacts should be stored outside PostgreSQL.

Initial development storage:

**MinIO**

Potential production storage:

- Amazon S3
- Azure Blob Storage

Stored artifacts may include:

```text
Original PDFs
Page Images
OCR Output
Processed Documents
Evaluation Artifacts
```

---

# 22. Caching

Redis will initially be used for caching.

The system should support:

### Exact Response Cache

Identical queries can reuse previous results when safe.

### Semantic Cache

Semantically similar queries may reuse cached responses when the underlying evidence and system state are compatible.

### Application Cache

Cache frequently accessed:

- Scripture metadata
- Search results
- Configuration
- Sessions

### Rate Limiting

Redis may also be used to enforce API rate limits.

---

# 23. Background Processing

Heavy operations must not block API requests.

Background processing will be used for:

- PDF processing
- OCR
- Page extraction
- Scripture parsing
- Embedding generation
- Vector indexing
- Evaluation
- Other long-running tasks

Initial implementation:

```text
FastAPI
   ↓
Redis
   ↓
Celery Workers
```

A durable workflow engine such as Temporal may be introduced later if processing complexity requires it.

---

# 24. Admin Dashboard

Administrators should be able to monitor:

### Users

- Total users
- Active users
- Roles
- Organizations

### Documents

- Total documents
- Processing status
- Failed documents
- OCR confidence
- Processing history

### AI System

- Queries
- Latency
- Model usage
- Cache hit rate
- Retrieval performance

### System

- API health
- Worker health
- Database health
- Vector database health
- Storage health

---

# 25. Audit Logging

Security-sensitive and administrative operations must be logged.

Examples:

```text
LOGIN
LOGOUT
DOCUMENT_UPLOAD
DOCUMENT_DELETE
DOCUMENT_PROCESSING
OCR_REVIEW
USER_CREATED
ROLE_CHANGED
ADMIN_ACTION
CHAT_REQUEST
```

Audit records should include appropriate metadata such as:

- User
- Action
- Resource
- Timestamp
- Result

---

# 26. Observability

The platform should provide end-to-end observability.

### Application

- Structured logs
- Error tracking
- Request metrics

### Infrastructure

- CPU
- Memory
- GPU
- Database
- Redis
- Qdrant
- Worker health

### AI pipeline

- Retrieval latency
- Reranking latency
- LLM latency
- Token usage
- Cache hit rate
- Context size

Target technologies:

```text
OpenTelemetry
Prometheus
Grafana
Loki
LangSmith
```

---

# 27. AI Evaluation

The system must include an evaluation framework.

## OCR Evaluation

- Character Error Rate
- Word Error Rate
- Verse extraction accuracy

## Retrieval Evaluation

- Recall@K
- Precision@K
- MRR
- NDCG

## RAG Evaluation

- Faithfulness
- Answer relevance
- Context precision
- Context recall
- Citation accuracy

## System Evaluation

- P50 latency
- P95 latency
- Error rate
- Cache hit rate

---

# 28. Security Requirements

The application should follow secure development practices.

Requirements include:

- HTTPS/TLS in deployed environments
- Secure authentication
- RBAC
- Input validation
- API rate limiting
- Request-size limits
- Secure CORS configuration
- Secret management
- Database access controls
- Audit logging
- Dependency vulnerability scanning
- Container security scanning
- No secrets in Git

---

# 29. Multi-Tenancy

The architecture should be designed to support multiple organizations in the future.

Relevant records should support:

```text
organization_id
```

This allows future deployments such as:

```text
Organization A
 ├── Users
 ├── Documents
 └── Conversations

Organization B
 ├── Users
 ├── Documents
 └── Conversations
```

The first release may operate as a single-organization deployment while preserving this architectural capability.

---

# 30. Frontend Requirements

Technology:

```text
Next.js
TypeScript
Tailwind CSS
shadcn/ui
TanStack Query
Zustand
PDF.js
```

Primary pages:

```text
Landing Page
Login
Dashboard
Chat
Scripture Library
Scripture Viewer
Search
Bookmarks
Conversation History
Profile
Settings
Admin Dashboard
```

---

# 31. Scripture Viewer

The viewer should allow users to navigate:

```text
Scripture
 ↓
Volume
 ↓
Chapter
 ↓
Verse
```

The interface should support:

- Original Sanskrit
- Hindi translation
- English translation where available
- Commentary
- Page image
- Citation information

---

# 32. User Feedback

Users should be able to indicate:

- Helpful
- Not helpful
- Incorrect citation
- Incorrect answer
- OCR issue
- Missing source

Feedback should be stored and used for evaluation and future improvements.

---

# 33. Performance Requirements

Initial targets:

### API

- Typical API response: < 500 ms excluding LLM generation
- P95 API latency should be monitored

### Retrieval

- Target retrieval latency: < 1 second under local development conditions

### Chat

Streaming should begin as quickly as practical after retrieval/context preparation.

### Document Processing

Processing must be asynchronous and resumable.

Performance targets will be refined after benchmarking real scripture documents.

---

# 34. Reliability Requirements

The system should:

- Retry failed background jobs
- Preserve processing state
- Avoid duplicate document processing
- Support resumable ingestion
- Preserve original documents
- Maintain document versions
- Avoid data loss
- Provide health checks

A failed OCR operation should not require reprocessing an entire multi-volume corpus.

---

# 35. Development Environment

The project will use two development laptops.

## Primary AI/ML Workstation

**RISHABH laptop**

Responsibilities:

- OCR
- PDF processing
- Embeddings
- Reranking
- Local LLM
- RAG experiments
- Evaluation
- GPU workloads

## Application Engineering Workstation

**Primary user laptop**

Responsibilities:

- FastAPI
- PostgreSQL
- Authentication
- Keycloak
- Frontend
- API development
- Security
- Integration
- Documentation

Both machines will use the same Git repository and development configuration.

---

# 36. Source Code Management

GitHub will be the source-code repository.

Branch strategy:

```text
main
 │
 └── develop
      │
      ├── feature/authentication
      ├── feature/frontend
      ├── feature/ocr
      ├── feature/ingestion
      ├── feature/rag
      ├── feature/local-llm
      └── feature/evaluation
```

`main` will contain stable releases.

`develop` will contain integrated development work.

Feature branches will be used for individual changes.

---

# 37. Data Management Principle

Git must contain:

- Source code
- Configuration templates
- Database migrations
- Documentation
- Tests
- Infrastructure definitions

Git must not contain:

- Large scripture PDFs
- Page images
- OCR datasets
- Embedding databases
- Model weights
- Secrets
- Generated artifacts

The canonical data architecture will be:

```text
GitHub
  ↓
Code + Configuration

Object Storage
  ↓
Documents + Artifacts

PostgreSQL
  ↓
Application Metadata

Qdrant
  ↓
Vector Index
```

---

# 38. Enterprise Technology Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js + TypeScript |
| UI | Tailwind CSS + shadcn/ui |
| Backend | FastAPI |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Authentication | Keycloak + OIDC |
| Cache | Redis |
| Object Storage | MinIO → S3/Azure Blob |
| Vector DB | Qdrant |
| Search | BM25 + Dense Retrieval |
| Embeddings | BGE-M3 |
| Reranking | BGE Reranker |
| OCR | PaddleOCR + Tesseract |
| Image Processing | OpenCV |
| PDF Processing | PyMuPDF |
| Layout Processing | DocTR |
| Orchestration | LangGraph |
| Local LLM Runtime | Ollama |
| Local LLM | Hardware-dependent Qwen-family model |
| Background Jobs | Celery + Redis |
| API Gateway | Nginx/Traefik |
| Containers | Docker |
| CI/CD | GitHub Actions |
| Monitoring | Prometheus + Grafana |
| Logs | Loki |
| Tracing | OpenTelemetry |
| AI Observability | LangSmith |
| Evaluation | RAGAS + DeepEval |
| Testing | Pytest + Playwright |
| Secrets | Vault / Cloud Secret Manager |
| IaC | Terraform |
| Future deployment | Kubernetes |

---

# 39. High-Level System Architecture

```text
                         USER
                           │
                           ▼
                    Next.js Frontend
                           │
                           ▼
                    API Gateway
                           │
                           ▼
                       FastAPI
                           │
             ┌─────────────┼──────────────┐
             │             │              │
             ▼             ▼              ▼
         Keycloak       PostgreSQL       Redis
             │                            │
             │                            │
             │                       Cache / Queue
             │                            │
             │                            ▼
             │                      Background Workers
             │                            │
             │                            ▼
             │                     Document Pipeline
             │                            │
             │                            ▼
             │                     OCR / Parsing
             │                            │
             │                            ▼
             │                       Embeddings
             │                            │
             │                            ▼
             │                          Qdrant
             │
             │
             └──────────────────────────────┐
                                            ▼
                                      LangGraph
                                            │
                                      Hybrid RAG
                                            │
                                        Reranker
                                            │
                                            ▼
                                       Local LLM
                                            │
                                            ▼
                                   Citation Validator
                                            │
                                            ▼
                                       Final Answer
```

---

# 40. Document Intelligence Architecture

```text
Original PDF
     │
     ▼
Object Storage
     │
     ▼
PDF Processor
     │
     ▼
Page Images
     │
     ▼
Image Preprocessing
     │
     ▼
OCR
     │
     ▼
Layout Detection
     │
     ▼
Language Detection
     │
     ▼
Scripture Parser
     │
     ▼
Structured Scripture
     │
     ▼
Quality Validation
     │
     ├── High Confidence ──► Embeddings
     │
     └── Low Confidence ───► Human Review
```

---

# 41. Development Phases

## Phase 0 — Engineering Foundation

- Repository
- Git workflow
- Project structure
- Docker
- WSL2
- Environment configuration
- Documentation

## Phase 1 — Core Infrastructure

- PostgreSQL
- Redis
- Qdrant
- MinIO
- FastAPI
- Next.js

## Phase 2 — Authentication & Security

- Keycloak
- OIDC
- JWT
- RBAC
- Protected APIs
- Audit logging

## Phase 3 — Document Management

- PDF upload
- Object storage
- Document metadata
- Document versions
- Processing state

## Phase 4 — OCR & Document Intelligence

- PDF processing
- OpenCV
- Sanskrit/Hindi OCR
- Layout detection
- OCR confidence
- Scripture parsing

## Phase 5 — Scripture Knowledge Base

- Verse entities
- Chapter relationships
- Translation relationships
- Commentary relationships
- Metadata

## Phase 6 — Search & Retrieval

- BGE-M3
- Qdrant
- BM25
- Hybrid retrieval
- RRF
- Reranking

## Phase 7 — Local LLM

- Ollama
- Hardware-appropriate local model
- LLM abstraction
- Streaming
- Prompt management
- Caching

## Phase 8 — RAG

- Query analysis
- Retrieval
- Context selection
- Generation
- Citation generation
- Citation validation

## Phase 9 — Agentic System

- LangGraph
- Query router
- Retrieval agent
- Validation
- Response generation
- Safety checks

## Phase 10 — User Application

- Chat
- Search
- Scripture viewer
- Citations
- History
- Bookmarks
- Feedback

## Phase 11 — Evaluation

- Golden datasets
- OCR evaluation
- Retrieval evaluation
- RAG evaluation
- Citation evaluation

## Phase 12 — Observability

- OpenTelemetry
- Prometheus
- Grafana
- Loki
- LangSmith

## Phase 13 — Production

- Docker
- CI/CD
- Security scanning
- Cloud deployment
- Terraform
- Kubernetes where justified

---

# 42. MVP Definition

The first meaningful MVP is considered complete when a user can:

1. Create an account.
2. Log in securely.
3. Search the available scripture corpus.
4. Ask a question in English or Hindi.
5. Retrieve relevant Sanskrit/Hindi scripture passages.
6. Receive an answer from the local LLM.
7. See the supporting scripture citation.
8. Open the corresponding source/page.
9. Continue the conversation.
10. View conversation history.

The ingestion side of the MVP must support:

```text
Scanned PDF
    ↓
OCR
    ↓
Structured Scripture
    ↓
Embeddings
    ↓
Qdrant
    ↓
RAG
```

---

# 43. Success Criteria

Know Your Dharma v1.0 should demonstrate:

### Product

- Users can securely interact with the platform.
- Scripture can be searched across languages.
- Answers provide source evidence.
- Original source material remains accessible.

### AI

- Retrieval is measurable.
- Responses are grounded.
- Citations are validated.
- Hallucinations are actively evaluated.

### Engineering

- Services are containerized.
- Application state is persisted.
- Background jobs are resilient.
- Authentication and authorization are implemented.
- Logs and metrics are available.
- Tests are automated.
- Code is version-controlled through GitHub.

### Enterprise

- RBAC
- Audit logging
- Secure secrets
- Multi-tenant-ready architecture
- Observability
- CI/CD
- Scalable storage
- Model abstraction
- Reproducible development environment

---

# 44. Future Roadmap

Potential future capabilities:

## Knowledge Graph

```text
Verse
 ├── Concept
 ├── Character
 ├── Location
 ├── Scripture
 └── Related Verse
```

Potential technology: Neo4j.

## Multilingual Expansion

- Marathi
- Gujarati
- Tamil
- Telugu
- Kannada
- Bengali
- Other languages

## Vision-Based Interaction

```text
User uploads photograph of scripture
          ↓
OCR
          ↓
Verse identification
          ↓
Explanation
```

## Voice

- Sanskrit pronunciation
- Audio recitation
- Speech-to-text
- Voice-based scripture assistant

## Comparative Research

Allow users to compare:

```text
Original Sanskrit
        │
Hindi Translation
        │
English Translation
        │
Different Commentaries
```

## Cross-Scripture Knowledge Graph

Enable queries such as:

> Find teachings related to Karma across the Bhagavad Gita and Upanishads.

---

# 45. Product Principles

The following principles should guide development.

### 1. Source First

The original scripture is the source of truth.

### 2. Evidence Before Generation

Retrieve evidence before asking the LLM to generate an answer.

### 3. Never Hide Uncertainty

If evidence is insufficient, say so.

### 4. Preserve Original Text

OCR output must never replace the original document.

### 5. Separate Source and Interpretation

Generated explanations must not be presented as scripture.

### 6. Reproducibility

The same source and processing pipeline should produce traceable results.

### 7. Security by Design

Authentication, authorization, audit logging, and secure data handling are part of the core architecture.

### 8. Model Agnostic

The platform should not be tightly coupled to a single LLM.

### 9. Hardware Agnostic

Local development should work on available hardware while allowing production GPU scaling.

### 10. Build for Measurement

OCR, retrieval, RAG, latency, and citation quality should all be measurable.

---

# 46. Initial Release Philosophy

Know Your Dharma should evolve in the following order:

```text
Reliable Sources
       ↓
Reliable Digitization
       ↓
Reliable Search
       ↓
Reliable Retrieval
       ↓
Reliable Generation
       ↓
Reliable Citations
       ↓
Enterprise Platform
```

The system should **not prioritize adding more AI agents before establishing the quality of the underlying scripture data and retrieval pipeline**.

The quality of the final answer is fundamentally dependent on the quality of:

```text
Source
  ↓
OCR
  ↓
Structure
  ↓
Retrieval
  ↓
Context
  ↓
Generation
```

Therefore, document intelligence and retrieval quality are first-class product capabilities.

---

## 47. Initial Product Milestone

The first major end-to-end demonstration should be:

> **Upload a scanned Sanskrit/Hindi scripture PDF → automatically process it → identify its structure → index the verses → ask a question → retrieve the relevant Sanskrit/Hindi evidence → generate a response using the local LLM → display the answer with exact scripture and page-level citations.**

This is the foundational capability around which the rest of Know Your Dharma will be built.