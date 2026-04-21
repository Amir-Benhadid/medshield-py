import pytest
from medshield import Sanitizer, sanitize


def test_basic_masking():
    text = "Patient SSN is 123-45-6789 and email is john@doe.com"
    res = sanitize(text)
    assert "123-45-6789" not in res
    assert "[SSN_0]" in res
    assert "[EMAIL_0]" in res


def test_deterministic_behavior():
    s = Sanitizer(options={"level": "MASK"})
    text = "John has 123-45-6789. Also 123-45-6789 is his."
    res = s.sanitize(text)
    # The same SSN should get the same token
    assert res.count("[SSN_0]") == 2


def test_synthesize_mode():
    s = Sanitizer(options={"level": "SYNTHESIZE"})
    text = "Contact me at 555-123-0199"
    res = s.sanitize(text)
    assert "555-123-0199" not in res
    assert any(char.isdigit() for char in res)


def test_medical_context_preservation():
    # ICD10 code should NOT be masked if preserveMedicalContext is True
    text = "Diagnosis: J45.909 (Asthma)"
    res = sanitize(text, options={"preserveMedicalContext": True})
    assert "J45.909" in res

    # Should be masked if preserveMedicalContext is False
    res_masked = sanitize(text, options={"preserveMedicalContext": False})
    assert "J45.909" not in res_masked
