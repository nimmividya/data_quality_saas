import csv
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

from config import SEED, START_DATE, DAYS, OUTPUT_DIR, INCIDENTS

def customer_for_pipeline(pipeline_id, pipelines, sources):
    p = next(p for p in pipelines if int(p["pipeline_id"]) == pipeline_id)
    source = next(s for s in sources if int(s["source_id"]) == int(p["source_id"]))
    return int(source["customer_id"])

def failure_probability(customer_id, date_value, pipeline_name):
    if customer_id == 13 and "Billing" in pipeline_name:
        week = (date_value - START_DATE).days // 7
        return [0.03, 0.05, 0.10, 0.18][min(week, 3)]

    if customer_id == 7 and "CRM" in pipeline_name:
        incident = INCIDENTS["crm_pipeline_outage"]
        if incident["start"] <= date_value <= incident["end"]:
            return 0.50

    return 0.04

def main():
    random.seed(SEED + 5)

    with (Path(OUTPUT_DIR) / "pipelines.csv").open(encoding="utf-8") as f:
        pipelines = list(csv.DictReader(f))
    with (Path(OUTPUT_DIR) / "data_sources.csv").open(encoding="utf-8") as f:
        sources = list(csv.DictReader(f))

    rows = []
    run_id = 1

    for day_offset in range(DAYS):
        day = START_DATE + timedelta(days=day_offset)

        for pipeline in pipelines:
            schedule = pipeline["schedule"]
            if schedule == "Hourly":
                runs_per_day = 24
            elif schedule == "Every 6 hours":
                runs_per_day = 4
            elif schedule == "Daily":
                runs_per_day = 1
            else:
                runs_per_day = 1 if day.weekday() == 6 else 0

            customer_id = customer_for_pipeline(
                int(pipeline["pipeline_id"]), pipelines, sources
            )
            p_fail = failure_probability(
                customer_id, day, pipeline["pipeline_name"]
            )

            for run_no in range(runs_per_day):
                if schedule == "Hourly":
                    hour = run_no
                elif schedule == "Every 6 hours":
                    hour = run_no * 6
                else:
                    hour = 2

                started = datetime(
                    day.year, day.month, day.day, hour, 0, 0,
                    tzinfo=timezone.utc
                )
                duration = random.randint(30, 900)
                completed = started + timedelta(seconds=duration)

                status = "Failed" if random.random() < p_fail else "Succeeded"
                records = random.randint(500, 50000)

                rows.append({
                    "run_id": run_id,
                    "pipeline_id": int(pipeline["pipeline_id"]),
                    "started_at": started.isoformat(),
                    "completed_at": completed.isoformat(),
                    "status": status,
                    "records_processed": records,
                    "error_message": (
                        random.choice([
                            "Connection timeout",
                            "Source unavailable",
                            "Schema validation failed",
                            "Authentication error",
                        ]) if status == "Failed" else ""
                    ),
                })
                run_id += 1

    path = Path(OUTPUT_DIR) / "pipeline_runs.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Created {path} ({len(rows)} rows)")

if __name__ == "__main__":
    main()
