import csv
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

from config import (
    SEED, START_DATE, DAYS, OUTPUT_DIR, INCIDENTS,
    CUSTOMER_PROFILES
)

def read_csv(name):
    with (Path(OUTPUT_DIR) / name).open(encoding="utf-8") as f:
        return list(csv.DictReader(f))

def customer_profile(customer_id, customers):
    row = next(c for c in customers if int(c["customer_id"]) == customer_id)
    return row["profile"]

def base_failure(customer_id, run_date, customers):
    profile = customer_profile(customer_id, customers)
    rate = CUSTOMER_PROFILES[profile]["base_failure_rate"]

    if profile == "Deteriorating":
        day = (run_date - START_DATE).days
        rate = [0.05, 0.07, 0.12, 0.20][min(day // 7, 3)]

    return rate

def incident_status(check, asset, run_date):
    customer_id = int(asset["customer_id"])
    asset_name = asset["asset_name"]
    dimension = check["dimension"]

    # Incident 1: missing customer IDs.
    i = INCIDENTS["missing_customer_ids"]
    if (
        customer_id == i["customer_id"]
        and asset_name == i["asset_name"]
        and i["start"] <= run_date <= i["end"]
        and dimension == "Completeness"
    ):
        return "FAIL"

    # Incident 2: duplicate order IDs.
    i = INCIDENTS["duplicate_order_ids"]
    if (
        customer_id == i["customer_id"]
        and asset_name == i["asset_name"]
        and i["start"] <= run_date <= i["end"]
        and dimension == "Uniqueness"
    ):
        return "FAIL"

    # Incident 3: invalid negative product prices.
    i = INCIDENTS["invalid_product_prices"]
    if (
        customer_id == i["customer_id"]
        and asset_name == i["asset_name"]
        and i["start"] <= run_date <= i["end"]
        and dimension == "Validity"
    ):
        return "FAIL"

    # Incident 4: stale customer payments.
    i = INCIDENTS["stale_payment_asset"]
    if (
        customer_id == i["customer_id"]
        and asset_name == i["asset_name"]
        and i["start"] <= run_date <= i["end"]
        and dimension == "Freshness"
    ):
        return "FAIL"

    return None

def main():
    random.seed(SEED + 6)

    customers = read_csv("customers.csv")
    sources = read_csv("data_sources.csv")
    assets = read_csv("data_assets.csv")
    checks = read_csv("quality_checks.csv")

    source_to_customer = {
        int(s["source_id"]): int(s["customer_id"]) for s in sources
    }
    pipeline_to_customer = {}
    with (Path(OUTPUT_DIR) / "pipelines.csv").open(encoding="utf-8") as f:
        for p in csv.DictReader(f):
            pipeline_to_customer[int(p["pipeline_id"])] = source_to_customer[int(p["source_id"])]

    asset_by_id = {int(a["asset_id"]): a for a in assets}

    rows = []
    result_id = 1

    # One result per check per day = 450 * 30 = 13,500.
    # This is intentionally moderate so the portfolio stays fast locally.
    # It can be increased later to multiple executions per day.
    for day_offset in range(DAYS):
        run_date = START_DATE + timedelta(days=day_offset)

        for check in checks:
            asset = asset_by_id[int(check["asset_id"])]
            customer_id = int(asset["customer_id"])

            forced = incident_status(check, asset, run_date)
            p_fail = base_failure(customer_id, run_date, customers)

            if forced is not None:
                status = forced
            else:
                status = "FAIL" if random.random() < p_fail else "PASS"

            records_checked = random.randint(1000, 100000)
            if status == "FAIL":
                failure_rate = round(random.uniform(0.01, 0.25), 4)
                failed_records = max(
                    1, int(records_checked * failure_rate)
                )
            else:
                failure_rate = round(random.uniform(0.0, 0.005), 4)
                failed_records = int(records_checked * failure_rate)

            run_time = datetime(
                run_date.year, run_date.month, run_date.day,
                3, 0, 0, tzinfo=timezone.utc
            )

            rows.append({
                "result_id": result_id,
                "check_id": int(check["check_id"]),
                "run_time": run_time.isoformat(),
                "status": status,
                "records_checked": records_checked,
                "failed_records": failed_records,
                "failure_rate": failure_rate,
                "execution_duration_ms": random.randint(50, 2500),
            })
            result_id += 1

    path = Path(OUTPUT_DIR) / "quality_results.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Created {path} ({len(rows)} rows)")

if __name__ == "__main__":
    main()
