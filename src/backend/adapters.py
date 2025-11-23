from typing import Dict, List


class AdapterRegistry:
    """Lightweight registry placeholder for adapters (providers, parsers, targets)."""

    def __init__(self, kind: str):
        self.kind = kind
        self._adapters: Dict[str, str] = {}

    def register(self, key: str, description: str) -> None:
        self._adapters[key] = description

    def list(self) -> List[str]:
        return list(self._adapters.keys())


provider_registry = AdapterRegistry("mail_provider")
provider_registry.register("gmail", "Gmail IMAP adapter")
provider_registry.register("generic_imap", "Fallback IMAP adapter")

parser_registry = AdapterRegistry("parser")
parser_registry.register("DE_DHL", "DHL parser")
parser_registry.register("DE_HERMES", "Hermes parser")
parser_registry.register("AMAZON_UK", "Amazon UK parser")

target_registry = AdapterRegistry("target")
target_registry.register("google_calendar", "Google Calendar adapter")
target_registry.register("calendar_ics", "ICS file writer")
target_registry.register("todo_generic", "Generic todo adapter")
target_registry.register("ntfy_push", "ntfy push adapter")
