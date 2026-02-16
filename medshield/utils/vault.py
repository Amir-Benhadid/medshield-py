import uuid
from typing import Dict
from faker import Faker


class TokenVault:
    def __init__(self):
        self.faker = Faker()
        self.mappings: Dict[str, str] = {}
        self.synthetic_cache: Dict[str, str] = {}
        self.counters: Dict[str, int] = {}

    def get_token(self, value: str, label: str) -> str:
        key = f"{label}:{value.lower()}"
        if key not in self.mappings:
            count = self.counters.get(label, 0)
            self.mappings[key] = f"[{label}_{count}]"
            self.counters[label] = count + 1
        return self.mappings[key]

    def get_synthetic(self, value: str, label: str) -> str:
        key = f"{label}:{value.lower()}"
        if key not in self.synthetic_cache:
            if label == "PERSON":
                self.synthetic_cache[key] = self.faker.name()
            elif label == "LOCATION":
                self.synthetic_cache[key] = self.faker.address().split("\n")[0]
            elif label == "PHONE":
                self.synthetic_cache[key] = self.faker.phone_number()
            elif label == "EMAIL":
                self.synthetic_cache[key] = self.faker.email()
            else:
                self.synthetic_cache[key] = f"Fake_{label}"
        return self.synthetic_cache[key]

    def reset(self):
        self.mappings.clear()
        self.synthetic_cache.clear()
        self.counters.clear()
