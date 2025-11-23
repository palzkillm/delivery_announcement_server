from datetime import date
from typing import Dict, List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

from .adapters import parser_registry, provider_registry, target_registry
from .config import AppConfig, get_app_config
from .models import DeliveryObject
from .storage import DeliveryStore


class DebugParseEmailRequest(BaseModel):
    raw_email: str
    parser_hint: Optional[str] = None


app = FastAPI(title="Delivery Announcement Server")

delivery_store = DeliveryStore()
app_config: AppConfig = get_app_config()


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/ping")
def ping() -> Dict[str, str]:
    return {"message": "pong"}


@app.get("/deliveries")
def list_deliveries() -> List[DeliveryObject]:
    return delivery_store.list_all()


@app.get("/deliveries/today")
def deliveries_today() -> List[DeliveryObject]:
    today = date.today()
    return delivery_store.list_for_date(today)


@app.get("/meta/adapters")
def meta_adapters() -> Dict[str, List[str]]:
    return {
        "providers": provider_registry.list(),
        "parsers": parser_registry.list(),
        "targets": target_registry.list(),
    }


@app.get("/meta/providers")
def meta_providers() -> List[str]:
    return provider_registry.list()


@app.get("/meta/parsers")
def meta_parsers() -> List[str]:
    return parser_registry.list()


@app.get("/meta/targets")
def meta_targets() -> List[str]:
    return target_registry.list()


@app.get("/meta/config")
def meta_config() -> AppConfig:
    return app_config


@app.post("/debug/parse-email")
def debug_parse_email(payload: DebugParseEmailRequest) -> Dict[str, object]:
    return {
        "parsed": False,
        "message": "Parser stubs not implemented in prototype.",
        "available_parsers": parser_registry.list(),
        "parser_hint": payload.parser_hint,
        "sample_hash": hash(payload.raw_email),
    }
