from typing import Any, List, Sequence
from .. import Sanitizer, SanitizerOptions

class MedShieldTransformer:
    """
    A LangChain document transformer that sanitizes medical PII/PHI.
    Usage:
        sanitizer = MedShieldTransformer(options={"level": "SYNTHESIZE"})
        sanitized_docs = sanitizer.transform_documents(docs)
    """
    def __init__(self, options: dict = None):
        self.sanitizer = Sanitizer(options)

    def transform_documents(self, documents: Sequence[Any], **kwargs: Any) -> Sequence[Any]:
        for doc in documents:
            doc.page_content = self.sanitizer.sanitize(doc.page_content)
        return documents

class MedShieldMiddleware:
    """
    A generic integration for Python AI SDKs (OpenAI, Anthropic).
    Intercepts and sanitizes text before sending to the model.
    """
    def __init__(self, options: dict = None):
        self.sanitizer = Sanitizer(options)

    def process_messages(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        for msg in messages:
            if "content" in msg:
                msg["content"] = self.sanitizer.sanitize(msg["content"])
        return messages
