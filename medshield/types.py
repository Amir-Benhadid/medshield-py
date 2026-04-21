from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field


class DetectionResult(BaseModel):
    text: str
    label: str
    start: int
    end: int
    sensitiveValue: str


class ProcessedResult(BaseModel):
    sanitizedText: str
    detections: List[DetectionResult]


SensitivityLevel = Literal["MASK", "SYNTHESIZE", "REDACT"]


class SanitizerOptions(BaseModel):
    level: SensitivityLevel = "MASK"
    preserveMedicalContext: bool = True
    session_id: Optional[str] = None
