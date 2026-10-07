import csv
import random
from datetime import datetime, timezone
from pathlib import Path

from config import SEED, COUNTS, SOURCE_SYSTEMS, OUTPUT_DIR

def main():
    random.seed(SEED + 1)

    customers = list(range(1, COUNTS["customers"] + 1))
    allocation = {cid: 2 for cid in customers}
    for cid in random.sample(customers, 10):
        allocation[cid] += 1

    rows = []
    source_id = 1

    for customer_id in customers:
        systems = random.sample(SOURCE_SYSTEMS, allocation[customer_id])
        for system_name, source_type in systems:
            rows.append({
                "source_id": source_id,
                "customer_id": customer_id,
                "source_name": system_name,
                "source_type": source_type,
                "created_at": datetime(
                    2025, 6, ((source_id - 1) % 25) + 1,
                    10, 0, 0, tzinfo=timezone.utc
                ).isoformat(),
                "status": "Active",
            })
            source_id += 1

    path = Path(OUTPUT_DIR) / "data_sources.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Created {path} ({len(rows)} rows)")

if __name__ == "__main__":
    main()
