# MedShield-Py
**Privacy-First Healthcare PII/PHI Sanitization Engine for the Age of Generative AI.**

MedShield-Py is a high-performance, modular Python library designed to detect, mask, and synthesize sensitive medical data (PHI/PII). It acts as an "invisible privacy firewall" for MedTech applications, AI agents, and clinical researchers, ensuring HIPAA-compliant data flows without sacrificing the utility of Large Language Models (LLMs).

---

## Key Features

*   **Multi-Layer Detection Engine**:
    *   **Regex Layer**: High-speed detection of deterministic patterns (SSNs, Emails, MRNs, Credit Cards, IP Addresses, etc.).
    *   **NLP Layer (NER)**: Context-aware entity extraction using `spaCy` to identify Names, Locations, and Organizations.
    *   **Medical Layer**: Dictionary-based lookup for clinical terminology, ICD-10 codes, and custom hospital vocabularies.
*   **Three Sensitivity Modes**:
    *   `REDACT`: Complete removal of data (e.g., `[SSN]`).
    *   `MASK`: Partial obfuscation with type labels (e.g., `[PERSON_0]`).
    *   `SYNTHESIZE`: Replaces real data with medically plausible, format-preserving fake data using `Faker`.
*   **Advanced AI Agent Support**:
    *   **Deterministic Tokenization**: Consistent mapping (e.g., "John Doe" always becomes `[PERSON_0]`) to maintain clinical reasoning across LLM chat turns.
    *   **Medical Context Preservation**: Intelligently strips identifiers while retaining medical conditions (Diabetes, Asthma) for research integrity.
*   **Agentic SDK Integrations**: Official middleware for the **OpenAI Python SDK** and **LangChain**.
*   **Built-in MCP Server**: Native support for the Model Context Protocol (MCP) to integrate directly into AI IDEs and agents via FastMCP.

---

## Installation

```bash
pip install medshield-py
```

*Note: For the NLP features, you must also install the spaCy language model:*
```bash
python -m spacy download en_core_web_sm
```

---

## Quick Start

```python
from medshield import Sanitizer

sanitizer = Sanitizer(options={"level": "MASK"})
input_text = "Patient John Doe (SSN: 111-22-3333) was admitted today."

result = sanitizer.scan(input_text)

print(result.sanitizedText)
# Output: Patient [PERSON_0] (SSN: [SSN_0]) was admitted today.

print(result.detections)
# Details about every entity found, including original value and indices.
```

---

## Advanced Usage

### 1. LangChain Integration
Protect prompts and document embeddings before they hit the cloud.

```python
from medshield.integrations.langchain import MedShieldTransformer
from langchain_community.document_loaders import TextLoader

loader = TextLoader("patient_record.txt")
docs = loader.load()

# Sanitize all documents before indexing into a Vector DB
sanitizer = MedShieldTransformer(options={"level": "SYNTHESIZE"})
sanitized_docs = sanitizer.transform_documents(docs)
```

### 2. MCP Server (Model Context Protocol)
Run MedShield as a system-wide service that AI Agents can call using the FastMCP framework.

```bash
# Start the server
medshield-mcp
```

---

## Architecture: Chain of Responsibility

MedShield-Py uses a modular pipeline where text flows through multiple specialized layers.

1.  **RegexLayer**: Handles patterns with strict formats.
2.  **NERLayer**: Uses NLP for context-sensitive entities like names.
3.  **MedicalLayer**: Matches clinical keywords and ICD codes.

Each layer contributes to a `ProcessedResult` object, aggregating all detections and performing safe string replacements from back-to-front to maintain character index integrity.

---

## Testing

MedShield-Py is thoroughly tested with `pytest`, covering deterministic generation, mask consistency, and NLP validation.

```bash
# Run the test suite
pytest
```

---

## Security & Privacy
This library is designed to help with HIPAA/GDPR compliance but does not guarantee it on its own. Always audit your LLM data pipelines. MedShield-Py processes all data **locally** and never sends your text to external servers (except for the synthetic data generators which are also local libraries).

---

## License
Apache License 2.0 (c) MedShield-Py Team
