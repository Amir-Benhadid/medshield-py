import re
from typing import List, Dict, Any
from ..types import DetectionResult, SanitizerOptions
from ..utils.vault import TokenVault


class MedicalLayer:
    def __init__(self):
        # A basic dictionary for clinical terminology and ICD-10.
        # In a real-world scenario, this might be loaded from a larger database.
        self.medical_terms = {
            r"\b[A-TV-Z][0-9][0-9AB]\.?[0-9A-TV-Z]{0,4}\b": "ICD10",
            r"\b(asthma|diabetes|hypertension|cancer|tumor|infarction)\b": "DIAGNOSIS",
            r"\b(lisinopril|metformin|albuterol|amoxicillin|omeprazole)\b": "MEDICATION",
        }

    def process(
        self, text: str, options: SanitizerOptions, vault: TokenVault
    ) -> Dict[str, Any]:
        detections: List[DetectionResult] = []

        # If preserveMedicalContext is True, we don't mask medical terms
        if options.preserveMedicalContext:
            return {"sanitizedText": text, "detections": detections}

        matches = []
        for pattern, label in self.medical_terms.items():
            for match in re.finditer(pattern, text, flags=re.IGNORECASE):
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
