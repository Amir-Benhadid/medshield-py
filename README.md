# MedShield-Py 🛡️

**Professional PII/PHI Sanitization for Medical AI Agents (Python Version)**

MedShield-Py is a high-performance, privacy-first library designed to protect sensitive patient data in AI-driven healthcare workflows. It mirrors the architecture of `medshield-js`, providing a consistent privacy layer across your entire stack.

## 🚀 Key Features

- **Deterministic Tokenization**: Replaces sensitive data (e.g., John Doe) with persistent IDs (e.g., `[PERSON_0]`) to maintain clinical context across conversation turns.
- **Medical Context Preservation**: Automatically detects and preserves medical codes (ICD-10, RXNORM) while scrubbing PII/PHI.
- **Agentic Middleware**: Drop-in integrations for **LangChain**, **OpenAI**, and newer AI frameworks.
- **Synthetic Data Engine**: Replaces real data with medically plausible fake data for developer environments.

## 📦 Installation

```bash
pip install medshield-py
```

## 🛠️ Quick Start

### Basic Sanitization
```python
from medshield import sanitize

text = "Patient John Doe (SSN: 123-45-6789) has asthma."
clean_text = sanitize(text)
# Output: "Patient [PERSON_0] (SSN: [SSN_0]) has asthma."
```

### LangChain Integration
```python
from medshield.integrations.langchain import MedShieldTransformer
from langchain_community.document_loaders import TextLoader

loader = TextLoader("patient_record.txt")
docs = loader.load()

# Sanitize all documents before indexing into a Vector DB
sanitizer = MedShieldTransformer(options={"level": "SYNTHESIZE"})
sanitized_docs = sanitizer.transform_documents(docs)
```

### Managed Session (Deterministic)
```python
from medshield import Sanitizer

s = Sanitizer(options={"level": "MASK"})
print(s.sanitize("Call John at 555-0101")) # [PERSON_0] at [PHONE_0]
print(s.sanitize("Is John home?"))        # Is [PERSON_0] home? (Identifies same person)
```

## 🛡️ Sanitization Levels

- **`MASK` (Default)**: Replaces data with consistent tokens like `[PERSON_0]`.
- **`SYNTHESIZE`**: Replaces real data with plausible fakes (e.g., "John Doe" -> "Robert Smith").
- **`REDACT`**: Simple redaction with type labels like `[PERSON]`.

## 📜 License

Apache License 2.0
