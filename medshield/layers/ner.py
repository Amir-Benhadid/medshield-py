import spacy
from typing import List, Dict, Any
from ..types import DetectionResult, SanitizerOptions
from ..utils.vault import TokenVault


class NERLayer:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Fallback or initialization warning (in a real app, you'd auto-download or raise a clear error)
            import warnings

            warnings.warn(
                "Spacy model 'en_core_web_sm' not found. NERLayer will be inactive. Run: python -m spacy download en_core_web_sm"
            )
            self.nlp = None

    def process(
        self, text: str, options: SanitizerOptions, vault: TokenVault
    ) -> Dict[str, Any]:
        detections: List[DetectionResult] = []

        if not self.nlp:
            return {"sanitizedText": text, "detections": detections}

        doc = self.nlp(text)

        # Collect entities that match PII categories
        target_labels = {
            "PERSON": "PERSON",
            "ORG": "ORGANIZATION",
            "GPE": "LOCATION",
            "LOC": "LOCATION",
        }

        matches = []
        for ent in doc.ents:
            if ent.label_ in target_labels:
                matches.append(
                    {
                        "start": ent.start_char,
                        "end": ent.end_char,
                        "text": ent.text,
                        "label": target_labels[ent.label_],
                    }
                )

        # Sort matches backwards
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
