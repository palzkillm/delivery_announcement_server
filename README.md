# delivery_announcement_server
Transfers delivery announcement mails into calendar/todolist, and announces via push notification


# Delivery Announcement Server

A modular backend service that reads delivery-related emails from one or multiple mail accounts, extracts delivery information, updates delivery status over time, and publishes the results to one or multiple target systems (calendar, todo list, push notifications, etc.).

This service is intended to run on lightweight hardware (e.g., Raspberry Pi 5) and is fully containerized via Docker.

---

## ✨ Core Responsibilities

1. **Read emails from multiple mail accounts**
   - At least Gmail must be supported (OAuth- or App-Password-based IMAP)
   - Additional providers should be pluggable through a mail-provider adapter layer
   - Each mail account can have its own parsing rules, enabled adapters, and target systems

2. **Extract deliveries and create initial delivery objects**
   - Parse shipment announcement emails (e.g. DHL, Amazon, Hermes, FedEx…)
   - Use an adapter-based system:
     - `DE_DHL`, `DE_HERMES`, `GLOBAL_FEDEX`, `UK_AMAZON`, ...
   - Each adapter knows:
     - How to detect relevant emails  
     - How to extract dates, tracking IDs, carrier, notes  
     - How to produce a normalized JSON representation   
       → `DeliveryObject`

3. **Update deliveries when detailed time windows arrive**
   - Many carriers send a “narrower window” update:
     - e.g., DHL: “Your parcel will arrive within the next 15 minutes”
   - The system should reprocess the email, match it to the *existing* `DeliveryObject`, and update:
     - time window  
     - status  
     - ETA confidence  
     - last-updated timestamp  

4. **Write results into multiple target systems**
   - Target adapters (pluggable):
     - Calendar (local ICS write or Google Calendar API)
     - Todo (local system or external API)
     - Push notifications (e.g. Pushover / ntfy / iOS Shortcut Webhooks)
     - Webhooks for custom systems
   - Multiple targets per delivery are allowed
   - Targets can be enabled per mail account or per delivery service

5. **Daily push notification**
   - Push system should **announce deliveries occurring today**
   - NOT when a new delivery is first recognized
   - NOT when updates come in
   - Trigger should be time-based (e.g., morning cron, local timezone)

---

## 📦 Architecture Overview

### Main Components

/src/backend/
app.py ← FastAPI
core/
delivery_model.py ← Normalized DeliveryObject
delivery_store.py ← Storage (SQLite for now)
time_utils.py
mail/
provider_gmail.py ← Gmail IMAP adapter
provider_imap.py ← Generic IMAP fallback
provider_registry.py ← Adapter registry
parsers/
de_dhl.py ← DHL parser
de_hermes.py
amazon_uk.py
registry.py ← Parser registry
targets/
calendar_google.py ← Google Calendar adapter
calendar_ics.py ← ICS file writer
todo_generic.py
push_ntfy.py ← Daily push adapter
registry.py ← Target registry
scheduler/
daily_push_job.py ← "deliveries today" notifier
mail_poll_job.py ← fetch + parse + update cycle


---

## 🧠 Data Flow

### 1. Poll Mail Accounts
- For each configured mail account:
  - Fetch unread or delivery-relevant mails
  - Run through carrier parser registry
  - Produce or update a `DeliveryObject`

### 2. Store Deliveries
Each delivery is saved in a lightweight internal store (SQLite):

{
id: string,
carrier: "DE_DHL",
tracking_id: "...",
date_expected: "2025-03-01",
time_window: "14:00-16:00",
status: "announced" | "updated" | "delivered",
mail_account: "<account-id>",
raw_metadata: { … },
last_update: timestamp
}


### 3. Publish to Targets
Based on configuration, each updated or new object can be sent to:
- Calendar
- Todo
- Push
- Custom webhook

Only the **daily push task** should notify about “deliveries happening today”.

---

## ⚙️ Configuration Model (concept)

A possible configuration file (YAML or ENV-based):

```yaml
mail_accounts:
  - id: gmail_marco
    provider: gmail
    credentials:
      type: app_password
      username: "marco@gmail.com"
      password: "${GMAIL_MARCO_APP_PASSWORD}"
    enabled_parsers:
      - DE_DHL
      - DE_HERMES
      - AMAZON_UK
    targets:
      - google_calendar
      - ntfy_push

  - id: gmail_partner
    provider: gmail
    credentials:
      type: oauth
      token_file: "/secrets/gmail_partner.json"
    enabled_parsers:
      - DE_DHL
    targets:
      - google_calendar

🚀 API Endpoints (initial)

These exist in the minimal prototype (FastAPI):

    GET /health

    GET /ping

    GET /deliveries
    Returns all known delivery objects

    GET /deliveries/today

    POST /debug/parse-email
    For manual parser testing later

🐳 Deployment
Development (local)

Use docker-compose.dev.yml, which builds from source.
Production (e.g., Raspberry Pi 5)

deploy/docker-compose.prod.yml will:

    pull prebuilt images from GHCR

    mount config + secrets

    run daily jobs via cron or an internal scheduler

🚫 What must NOT be in the repo

    Credentials, OAuth tokens, IMAP passwords

    Calendar API keys

    Push API tokens

Use .env or a secrets volume instead.


---