from typing import List, Dict, Union
from .types import SanitizerOptions, ProcessedResult, DetectionResult
from .utils.vault import TokenVault
from .layers.regex import RegexLayer


class Sanitizer:
    def __init__(self, options: Union[SanitizerOptions, dict] = None):
        if isinstance(options, dict):
            self.options = SanitizerOptions(**options)
        else:
            self.options = options or SanitizerOptions()

        self.vault = TokenVault()
        self.layers = [RegexLayer()]  # Add more layers as they are implemented

    def sanitize(self, text: str) -> str:
        res = self.scan(text)
        return res.sanitizedText

    def scan(self, text: str) -> ProcessedResult:
        current_text = text
        all_detections: List[DetectionResult] = []

        for layer in self.layers:
            result = layer.process(current_text, self.options, self.vault)
            current_text = result["sanitizedText"]
            all_detections.extend(result["detections"])

        return ProcessedResult(sanitizedText=current_text, detections=all_detections)

    def reset_context(self):
        self.vault.reset()


# Functional export
def sanitize(text: str, options: dict = None) -> str:
    s = Sanitizer(options)
    return s.sanitize(text)
