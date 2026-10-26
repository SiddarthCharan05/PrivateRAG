# 🔐 PrivateRAG

### Privacy-Aware Enterprise AI for Secure Internal Knowledge Retrieval

PrivateRAG is a privacy-aware Retrieval-Augmented Generation (RAG) prototype designed to demonstrate how organisations can use generative AI with internal company knowledge while maintaining access controls, personal-data awareness, local inference, and privacy-safe auditability.

The project uses a fictional German company, **NordWerk Solutions GmbH**, and entirely synthetic demonstration data.

---

## 🎯 Project Motivation

Organisations want to use generative AI with internal knowledge, but enterprise adoption introduces important challenges:

- How can confidential documents remain access-controlled?
- How can personal information be detected before processing?
- How can internal knowledge be queried without relying on a public cloud LLM?
- How can AI interactions be audited without unnecessarily storing sensitive prompts?
- How can generated answers remain grounded in authorised company information?

PrivateRAG explores these questions through a local, privacy-aware RAG architecture.

---

## 🏗️ Architecture

```text
Employee Question
        │
        ▼
┌───────────────────────┐
│ PII / Privacy Scanner │
│      Presidio         │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ Role-Based Access     │
│ Control               │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ Authorised Semantic   │
│ Retrieval             │
│ ChromaDB              │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ Local LLM             │
│ Llama 3.2 via Ollama  │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ Grounded Answer       │
│ + Authorised Sources  │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ Privacy-Safe Audit    │
│ Metadata              │
└───────────────────────┘
```

---

## 🔐 Key Features

### Local LLM

PrivateRAG uses **Llama 3.2 through Ollama**, allowing language-model inference to run locally.

### Retrieval-Augmented Generation

Internal documents are:

1. loaded from the local knowledge base,
2. divided into searchable chunks,
3. converted into embeddings,
4. stored in ChromaDB,
5. retrieved according to semantic relevance.

The LLM is instructed to answer using the retrieved company context rather than inventing unsupported company information.

### Role-Based Access Control

Retrieval is filtered according to the employee's role **before documents are provided to the language model**.

Example:

```text
General Employee → General documents
IT Employee      → General + IT
HR Employee      → General + HR
Finance Employee → General + Finance
```

This means an IT employee cannot retrieve an HR-only compensation document even when asking a semantically relevant question.

### PII Detection

Microsoft Presidio is used to identify supported personal-data categories in employee questions.

Current examples include:

- Person names
- Email addresses
- Phone numbers
- IBANs
- Credit-card numbers
- IP addresses

Detected PII values are not displayed in the main application's privacy diagnostics.

### Privacy Risk Classification

Questions receive a simple demonstration-level classification:

```text
LOW
MEDIUM
HIGH
```

For example, supported financial identifiers such as an IBAN are classified as high risk in the current prototype.

> This classification is a prototype heuristic and should not be interpreted as a legal or regulatory determination.

### Privacy-Safe Audit Logging

PrivateRAG records limited interaction metadata in SQLite.

The audit log stores:

- timestamp,
- employee role,
- privacy-risk classification,
- detected PII categories,
- number of retrieved chunks.

It deliberately does **not** store:

- the raw employee question,
- detected PII values,
- the generated answer.

---

## 🧪 Example: Access-Controlled Retrieval

Question:

```text
What is Anna Müller's salary?
```

### HR employee

The HR role can access:

```text
GENERAL + HR
```

PrivateRAG can therefore retrieve the synthetic HR compensation record and answer from the authorised context.

### IT or General employee

The HR document is excluded from retrieval.

PrivateRAG responds:

```text
I cannot answer this from the company information available to your role.
```

The same question therefore produces different accessible knowledge depending on authorisation.

---

## 🛠️ Technology Stack

- Python
- Streamlit
- LangChain
- ChromaDB
- Ollama
- Llama 3.2
- Sentence Transformers
- Microsoft Presidio
- spaCy
- SQLite

---

## 📁 Project Structure

```text
PrivateRAG/
│
├── data/
│   ├── finance/
│   ├── general/
│   ├── hr/
│   └── it/
│
├── src/
│   ├── access_control.py
│   ├── app.py
│   ├── audit_logger.py
│   ├── document_loader.py
│   ├── privacy_scanner.py
│   ├── rag.py
│   └── vector_store.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## ⚠️ Disclaimer

PrivateRAG is an educational and portfolio prototype.

NordWerk Solutions GmbH is fictional, and the repository uses synthetic demonstration data.

The project is designed to explore privacy-aware and data-sovereign enterprise AI patterns. It does **not** claim GDPR compliance, regulatory certification, or production readiness.

---

## 🚀 Planned Improvements

Future versions may include:

- Docker deployment
- Automated tests
- PDF ingestion
- Improved document-level permissions
- Authentication
- More advanced privacy policies
- Retrieval confidence controls
- Improved citation metadata
- Administrative audit dashboard

---

## 👤 Author

**Charan Siddarth**

Data Science | AI | Data Analytics

Germany