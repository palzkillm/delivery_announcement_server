from typing import List

from pydantic import BaseModel


class MailAccountConfig(BaseModel):
    id: str
    provider_key: str
    display_name: str
    enabled: bool = True


class TargetConfig(BaseModel):
    id: str
    target_key: str
    display_name: str
    enabled: bool = True


class RoutingRuleConfig(BaseModel):
    id: str
    description: str
    mail_account_id: str
    parser_key: str
    target_ids: List[str]


class AppConfig(BaseModel):
    mail_accounts: List[MailAccountConfig]
    targets: List[TargetConfig]
    routing_rules: List[RoutingRuleConfig]


def get_app_config() -> AppConfig:
    mail_accounts = [
        MailAccountConfig(
            id="gmail_marco",
            provider_key="gmail",
            display_name="Marco Gmail",
            enabled=True,
        ),
        MailAccountConfig(
            id="gmail_partner",
            provider_key="gmail",
            display_name="Partner Gmail",
            enabled=True,
        ),
    ]

    targets = [
        TargetConfig(
            id="ntfy_daily",
            target_key="ntfy_push",
            display_name="ntfy daily push",
            enabled=True,
        ),
        TargetConfig(
            id="calendar_home",
            target_key="calendar_ics",
            display_name="Home ICS calendar",
            enabled=True,
        ),
    ]

    routing_rules = [
        RoutingRuleConfig(
            id="rule-dhl-marco",
            description="Marco DHL deliveries to ntfy and calendar",
            mail_account_id="gmail_marco",
            parser_key="DE_DHL",
            target_ids=["ntfy_daily", "calendar_home"],
        ),
        RoutingRuleConfig(
            id="rule-hermes-partner",
            description="Partner Hermes deliveries to calendar",
            mail_account_id="gmail_partner",
            parser_key="DE_HERMES",
            target_ids=["calendar_home"],
        ),
    ]

    return AppConfig(
        mail_accounts=mail_accounts,
        targets=targets,
        routing_rules=routing_rules,
    )
