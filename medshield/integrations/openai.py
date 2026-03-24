from typing import Any, Dict, List
from .. import Sanitizer

class OpenAIMedShieldMiddleware:
    """
    Middleware for intercepting and sanitizing messages sent to the OpenAI Python SDK.
    """
    def __init__(self, options: dict = None):
        self.sanitizer = Sanitizer(options)

    def sanitize_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Takes a list of OpenAI chat completion messages and sanitizes their content.
        """
        sanitized = []
        for msg in messages:
            # Create a copy so we don't mutate the original dictionary
            clean_msg = dict(msg)
            if "content" in clean_msg and isinstance(clean_msg["content"], str):
                clean_msg["content"] = self.sanitizer.sanitize(clean_msg["content"])
            sanitized.append(clean_msg)
        return sanitized
