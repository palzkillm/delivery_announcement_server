from datetime import date, datetime
from typing import Dict, Optional

from pydantic import BaseModel, Field


Status = str


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
