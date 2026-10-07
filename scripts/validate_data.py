import csv
from pathlib import Path
from collections import Counter

OUTPUT = Path(__file__).resolve().parent.parent / "data"

EXPECTED = {
    "customers.csv": 20,
    "data_sources.csv": 50,
    "pipelines.csv": 75,
    "data_assets.csv": 150,
    "quality_checks.csv": 450,
    "pipeline_runs.csv": None,
    "quality_results.csv": 13500,
}

def read(name):
    with (OUTPUT / name).open(encoding="utf-8") as f:
        return list(csv.DictReader(f))

def main():
    data = {name: read(name) for name in EXPECTED}

    print("=== Row counts ===")
    for name, expected in EXPECTED.items():
        actual = len(data[name])
        if expected is None:
            print(f"{name}: {actual:,}")
        else:
            print(f"{name}: {actual:,}  expected={expected:,}  "
                  f"{'OK' if actual == expected else 'ERROR'}")

    print("\n=== Key distributions ===")
    print("Plans:", Counter(r["plan"] for r in data["customers.csv"]))
    print("Customer status:", Counter(r["status"] for r in data["customers.csv"]))
    print("Pipeline schedules:", Counter(r["schedule"] for r in data["pipelines.csv"]))
    print("Asset criticality:", Counter(r["criticality"] for r in data["data_assets.csv"]))
    print("Check dimensions:", Counter(r["dimension"] for r in data["quality_checks.csv"]))
    print("Quality result status:", Counter(r["status"] for r in data["quality_results.csv"]))

    print("\n=== Incident checks ===")
    # Join results through checks -> assets -> customers.
    checks = {int(r["check_id"]): r for r in data["quality_checks.csv"]}
    assets = {int(r["asset_id"]): r for r in data["data_assets.csv"]}

    incident_targets = [
        (7, "customer_orders", "Completeness"),
        (13, "customer_orders", "Uniqueness"),
        (18, "product_catalog", "Validity"),
        (18, "customer_payments", "Freshness"),
    ]

    for customer_id, asset_name, dimension in incident_targets:
        matches = 0
        fails = 0
        for result in data["quality_results.csv"]:
            check = checks[int(result["check_id"])]
            asset = assets[int(check["asset_id"])]
            if (
                int(asset["customer_id"]) == customer_id
                and asset["asset_name"] == asset_name
                and check["dimension"] == dimension
            ):
                matches += 1
                fails += result["status"] == "FAIL"
        print(
            f"Customer {customer_id:02d} / {asset_name} / {dimension}: "
            f"{fails}/{matches} FAIL"
        )

if __name__ == "__main__":
    main()
