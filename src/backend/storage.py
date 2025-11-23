from datetime import date
from typing import List

from .models import DeliveryObject


class DeliveryStore:
    """Simple in-memory delivery storage."""

    def __init__(self) -> None:
        self._deliveries: List[DeliveryObject] = [
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

    def list_all(self) -> List[DeliveryObject]:
        return list(self._deliveries)

    def list_for_date(self, date_expected: date) -> List[DeliveryObject]:
        return [delivery for delivery in self._deliveries if delivery.date_expected == date_expected]

    def add(self, delivery: DeliveryObject) -> None:
        self._deliveries.append(delivery)
