import csv
import random
from datetime import datetime, timezone
from pathlib import Path

from config import (
    SEED, COUNTS, PLAN_COUNTS, CUSTOMER_STATUS_COUNTS,
    CUSTOMER_PROFILES, OUTPUT_DIR
)

def weighted_profiles():
    profiles = []
    for profile, cfg in CUSTOMER_PROFILES.items():
        profiles.extend([profile] * cfg["count"])
    return profiles

def main():
    random.seed(SEED)
    output = Path(OUTPUT_DIR)
    output.mkdir(parents=True, exist_ok=True)

    profiles = weighted_profiles()
    random.shuffle(profiles)

    plans = []
    for plan, count in PLAN_COUNTS.items():
        plans.extend([plan] * count)
    random.shuffle(plans)

    statuses = []
    for status, count in CUSTOMER_STATUS_COUNTS.items():
        statuses.extend([status] * count)
    random.shuffle(statuses)

    rows = []
    for customer_id in range(1, COUNTS["customers"] + 1):
        created_at = datetime(
            2025 + (customer_id % 2),
            ((customer_id - 1) % 12) + 1,
            ((customer_id * 3) % 25) + 1,
            9, 0, 0, tzinfo=timezone.utc
        )

        rows.append({
            "customer_id": customer_id,
            "customer_name": f"Customer {customer_id:02d}",
            "plan": plans[customer_id - 1],
            "status": statuses[customer_id - 1],
            "created_at": created_at.isoformat(),
            "profile": profiles[customer_id - 1],
        })

    path = output / "customers.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Created {path} ({len(rows)} rows)")

if __name__ == "__main__":
    main()
