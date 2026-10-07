from datetime import date

SEED = 42
START_DATE = date(2026, 9, 6)
DAYS = 30

OUTPUT_DIR = "data"

COUNTS = {
    "customers": 20,
    "sources": 50,
    "pipelines": 75,
    "assets": 150,
    "checks": 450,
}

PLAN_COUNTS = {
    "Starter": 6,
    "Professional": 9,
    "Enterprise": 5,
}

CUSTOMER_STATUS_COUNTS = {
    "Active": 18,
    "Suspended": 1,
    "Churned": 1,
}

CUSTOMER_PROFILES = {
    "Excellent": {"count": 4, "base_failure_rate": 0.03},
    "Healthy": {"count": 8, "base_failure_rate": 0.06},
    "Problematic": {"count": 5, "base_failure_rate": 0.10},
    "Deteriorating": {"count": 2, "base_failure_rate": 0.12},
    "Critical": {"count": 1, "base_failure_rate": 0.18},
}

SOURCE_TYPES = [
    "CRM", "Database", "E-commerce", "Finance",
    "HR", "Marketing", "Support"
]

SOURCE_SYSTEMS = [
    ("Salesforce", "CRM"),
    ("HubSpot", "CRM"),
    ("PostgreSQL", "Database"),
    ("MySQL", "Database"),
    ("Shopify", "E-commerce"),
    ("Stripe", "Finance"),
    ("Workday", "HR"),
    ("NetSuite", "Finance"),
    ("Google Analytics", "Marketing"),
    ("Zendesk", "Support"),
]

SCHEDULES = {
    "Hourly": 60,
    "Every 6 hours": 360,
    "Daily": 1440,
    "Weekly": 10080,
}

ASSET_NAMES = [
    "customer_accounts", "customer_contacts", "customer_orders",
    "customer_payments", "products", "product_catalog",
    "subscriptions", "invoices", "employees",
    "marketing_campaigns", "support_tickets",
]

ASSET_TYPES = ["Table", "View", "Dataset"]

CRITICALITIES = ["Low", "Medium", "High", "Critical"]

QUALITY_DIMENSIONS = [
    "Completeness", "Accuracy", "Validity",
    "Uniqueness", "Consistency", "Freshness"
]

SEVERITIES = ["Low", "Medium", "High", "Critical"]

CHECK_TEMPLATES = {
    "Completeness": [
        ("{field} NOT NULL", "not_null"),
    ],
    "Accuracy": [
        ("{field} accuracy", "accuracy"),
    ],
    "Validity": [
        ("{field} valid", "validity"),
        ("{field} >= 0", "non_negative"),
    ],
    "Uniqueness": [
        ("{field} UNIQUE", "unique"),
    ],
    "Consistency": [
        ("{field} consistent", "consistency"),
    ],
    "Freshness": [
        ("{asset} refreshed within SLA", "freshness"),
    ],
}

FIELDS_BY_ASSET = {
    "customer_accounts": ["customer_id", "customer_name"],
    "customer_contacts": ["contact_id", "customer_id"],
    "customer_orders": ["order_id", "customer_id", "order_date", "order_amount"],
    "customer_payments": ["payment_id", "customer_id", "payment_date", "amount"],
    "products": ["product_id", "product_name", "price"],
    "product_catalog": ["product_id", "product_name", "product_price"],
    "subscriptions": ["subscription_id", "customer_id", "start_date", "status"],
    "invoices": ["invoice_id", "customer_id", "invoice_date", "amount"],
    "employees": ["employee_id", "employee_name", "department"],
    "marketing_campaigns": ["campaign_id", "campaign_name", "start_date"],
    "support_tickets": ["ticket_id", "customer_id", "created_at", "status"],
}

# Explicit synthetic incidents. Keeping these in configuration makes the
# portfolio project easy to explain and reproduce.
INCIDENTS = {
    "missing_customer_ids": {
        "customer_id": 7,
        "asset_name": "customer_orders",
        "start": date(2026, 9, 15),
        "end": date(2026, 9, 18),
    },
    "duplicate_order_ids": {
        "customer_id": 13,
        "asset_name": "customer_orders",
        "start": date(2026, 9, 20),
        "end": date(2026, 9, 24),
    },
    "invalid_product_prices": {
        "customer_id": 18,
        "asset_name": "product_catalog",
        "start": date(2026, 9, 25),
        "end": date(2026, 10, 2),
    },
    "stale_payment_asset": {
        "customer_id": 18,
        "asset_name": "customer_payments",
        "start": date(2026, 9, 28),
        "end": date(2026, 10, 1),
        "freshness_hours": 30,
    },
    "billing_pipeline_deterioration": {
        "customer_id": 13,
        "pipeline_keyword": "Billing",
    },
    "crm_pipeline_outage": {
        "customer_id": 7,
        "pipeline_keyword": "CRM",
        "start": date(2026, 9, 24),
        "end": date(2026, 9, 26),
    },
}
