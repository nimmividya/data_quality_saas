import csv
import random
from datetime import datetime, timezone
from pathlib import Path

from config import (
    SEED, COUNTS, ASSET_NAMES, ASSET_TYPES, CRITICALITIES, OUTPUT_DIR
)


# Required assets for the intentional data-quality incidents.
REQUIRED_ASSETS = {
    7: ["customer_orders"],
    13: ["customer_orders"],
    18: ["product_catalog", "customer_payments"],
}


def main():
    random.seed(SEED + 3)

    output_dir = Path(OUTPUT_DIR)

    with (output_dir / "pipelines.csv").open(encoding="utf-8") as f:
        pipelines = list(csv.DictReader(f))

    with (output_dir / "data_sources.csv").open(encoding="utf-8") as f:
        sources = list(csv.DictReader(f))

    rows = []
    asset_id = 1

    for customer_id in range(1, COUNTS["customers"] + 1):

        # Each customer gets 7 or 8 assets.
        n_assets = 8 if customer_id <= 10 else 7

        required_names = REQUIRED_ASSETS.get(customer_id, [])

        # Select the remaining asset names randomly.
        available_names = [
            name
            for name in ASSET_NAMES
            if name not in required_names
        ]

        remaining_count = n_assets - len(required_names)

        names = required_names + random.sample(
            available_names,
            remaining_count
        )

        # Find this customer's sources.
        customer_source_ids = {
            int(s["source_id"])
            for s in sources
            if int(s["customer_id"]) == customer_id
        }

        customer_pipelines = [
            p for p in pipelines
            if int(p["source_id"]) in customer_source_ids
        ]

        if not customer_pipelines:
            raise ValueError(
                f"No pipelines found for Customer {customer_id}"
            )

        for name in names:

            pipeline = random.choice(customer_pipelines)

            criticality = random.choices(
                CRITICALITIES,
                weights=[20, 35, 30, 15],
                k=1
            )[0]

            if name in {
                "customer_payments",
                "customer_orders",
                "invoices"
            }:
                refresh_hours = 24

            elif name in {
                "support_tickets",
                "customer_contacts"
            }:
                refresh_hours = 12

            elif name == "marketing_campaigns":
                refresh_hours = 168

            else:
                refresh_hours = 24

            rows.append({
                "asset_id": asset_id,
                "customer_id": customer_id,
                "pipeline_id": int(pipeline["pipeline_id"]),
                "asset_name": name,
                "asset_type": random.choice(ASSET_TYPES),
                "criticality": criticality,
                "expected_refresh_hours": refresh_hours,
                "status": "Active",
                "created_at": datetime(
                    2025,
                    8,
                    ((asset_id - 1) % 25) + 1,
                    7,
                    0,
                    0,
                    tzinfo=timezone.utc
                ).isoformat(),
            })

            asset_id += 1

    # Make sure we still have exactly 150 assets.
    assert len(rows) == COUNTS["assets"], len(rows)

    path = output_dir / "data_assets.csv"

    with path.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=rows[0].keys()
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"Created {path} ({len(rows)} rows)")


if __name__ == "__main__":
    main()