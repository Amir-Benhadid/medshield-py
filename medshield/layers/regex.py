import re
from typing import List, Dict
from ..types import DetectionResult, SanitizerOptions
from ..utils.vault import TokenVault


class RegexLayer:
    def __init__(self):
        self.patterns = {
            "EMAIL": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "PHONE": r"\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}",
            "SSN": r"\d{3}-\d{2}-\d{4}",
            "ICD10": r"[A-TV-Z][0-9][0-9AB]\.?[0-9A-TV-Z]{0,4}",
            "MRN": r"\bMRN-?\d{6,10}\b",
        }

    def process(
        self, text: str, options: SanitizerOptions, vault: TokenVault
    ) -> Dict[str, any]:
        detections: List[DetectionResult] = []

        # Collect all matches
        matches = []
        for label, pattern in self.patterns.items():
            for match in re.finditer(pattern, text):
                # Skip ICD10 if we want to preserve medical context
                if label == "ICD10" and options.preserveMedicalContext:
                    continue

                matches.append(
                    {
                        "start": match.start(),
                        "end": match.end(),
                        "text": match.group(),
                        "label": label,
                    }
                )

        # Sort matches backwards to avoid index shifting during replacement
        matches.sort(key=lambda x: x["start"], reverse=True)

        sanitized_text = text
        for m in matches:
            orig_value = m["text"]
            replacement = ""

            if options.level == "MASK":
                replacement = vault.get_token(orig_value, m["label"])
            elif options.level == "SYNTHESIZE":
                replacement = vault.get_synthetic(orig_value, m["label"])
            else:  # REDACT
                replacement = f"[{m['label']}]"

            sanitized_text = (
                sanitized_text[: m["start"]] + replacement + sanitized_text[m["end"] :]
            )

            detections.append(
                DetectionResult(
                    text=replacement,
                    label=m["label"],
                    start=m["start"],
                    end=m["start"] + len(replacement),
                    sensitiveValue=orig_value,
                )
            )

        return {"sanitizedText": sanitized_text, "detections": detections}
