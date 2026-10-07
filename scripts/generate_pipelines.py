import csv
import random
from datetime import datetime, timezone
from pathlib import Path

from config import SEED, COUNTS, SCHEDULES, OUTPUT_DIR

def main():
    random.seed(SEED + 2)

    with (Path(OUTPUT_DIR) / "data_sources.csv").open(encoding="utf-8") as f:
        sources = list(csv.DictReader(f))

    rows = []
    pipeline_id = 1

    # Exactly 75 pipelines: 25 sources receive 2 pipelines, 25 receive 1.
    sources_for_two = set(random.sample(range(len(sources)), 25))

    for idx, source in enumerate(sources):
        n = 2 if idx in sources_for_two else 1

        for seq in range(1, n + 1):
            source_name = source["source_name"]
            if source["customer_id"] == "13" and seq == 1:
                pipeline_name = "Billing Pipeline"
            elif source["customer_id"] == "7" and source_name in {"Salesforce", "HubSpot"} and seq == 1:
                pipeline_name = "CRM Pipeline"
            else:
                pipeline_name = f"{source_name} Pipeline {seq}"

            schedule = random.choices(
                list(SCHEDULES.keys()),
                weights=[40, 20, 35, 5],
                k=1
            )[0]

            rows.append({
                "pipeline_id": pipeline_id,
                "source_id": int(source["source_id"]),
                "pipeline_name": pipeline_name,
                "schedule": schedule,
                "expected_frequency_minutes": SCHEDULES[schedule],
                "status": "Active",
                "created_at": datetime(
                    2025, 7, ((pipeline_id - 1) % 25) + 1,
                    8, 0, 0, tzinfo=timezone.utc
                ).isoformat(),
            })
            pipeline_id += 1

    # Defensive check: the project contract calls for 75 pipelines.
    assert len(rows) == COUNTS["pipelines"], len(rows)

    path = Path(OUTPUT_DIR) / "pipelines.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Created {path} ({len(rows)} rows)")

if __name__ == "__main__":
    main()
