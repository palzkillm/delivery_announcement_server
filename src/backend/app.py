from datetime import date, datetime
from typing import Dict, List, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field


Status = str  # Minimal alias to keep implementation simple


class DeliveryObject(BaseModel):
    id: str
    carrier: str
    tracking_id: str
    date_expected: date
    time_window: Optional[str] = None
    status: Status
    mail_account: str
    raw_metadata: Dict[str, str] = Field(default_factory=dict)
    last_update: datetime = Field(default_factory=datetime.utcnow)


class AdapterRegistry:
    """Lightweight registry placeholder for adapters (providers, parsers, targets)."""

    def __init__(self, kind: str):
        self.kind = kind
        self._adapters: Dict[str, str] = {}

    def register(self, key: str, description: str) -> None:
        self._adapters[key] = description

    def list(self) -> List[str]:
        return list(self._adapters.keys())


class DebugParseEmailRequest(BaseModel):
    raw_email: str
    parser_hint: Optional[str] = None


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


app = FastAPI(title="Delivery Announcement Server")


_DELIVERIES: List[DeliveryObject] = [
    DeliveryObject(
        id="sample-1",
        carrier="DE_DHL",
        tracking_id="123456789",
        date_expected=date.today(),
        time_window="14:00-16:00",
        status="announced",
        mail_account="gmail_marco",
    ),
    DeliveryObject(
        id="sample-2",
        carrier="DE_HERMES",
        tracking_id="HERMES-987654",
        date_expected=date.today(),
        time_window=None,
        status="updated",
        mail_account="gmail_partner",
    ),
]


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/ping")
def ping() -> Dict[str, str]:
    return {"message": "pong"}


@app.get("/deliveries")
def list_deliveries() -> List[DeliveryObject]:
    return _DELIVERIES


@app.get("/deliveries/today")
def deliveries_today() -> List[DeliveryObject]:
    today = date.today()
    return [delivery for delivery in _DELIVERIES if delivery.date_expected == today]


@app.post("/debug/parse-email")
def debug_parse_email(payload: DebugParseEmailRequest) -> Dict[str, object]:
    return {
        "parsed": False,
        "message": "Parser stubs not implemented in prototype.",
        "available_parsers": parser_registry.list(),
        "parser_hint": payload.parser_hint,
        "sample_hash": hash(payload.raw_email),
    }
