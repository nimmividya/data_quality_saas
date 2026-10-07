import csv
import random
from datetime import datetime, timezone
from pathlib import Path

from config import (
    SEED, COUNTS, QUALITY_DIMENSIONS, SEVERITIES,
    FIELDS_BY_ASSET, OUTPUT_DIR
)


# Required checks for the intentional data-quality incidents.
REQUIRED_CHECKS = [
    (7, "customer_orders", "Completeness"),
    (13, "customer_orders", "Uniqueness"),
    (18, "product_catalog", "Validity"),
    (18, "customer_payments", "Freshness"),
]


def build_check(asset, dimension, check_id):
    asset_name = asset["asset_name"]
    fields = FIELDS_BY_ASSET.get(asset_name, ["record_id", "status"])

    field = random.choice(fields)

    if dimension == "Freshness":
        check_name = f"{asset_name} refreshed within SLA"
        check_type = "freshness"
        threshold = int(asset["expected_refresh_hours"])

    elif dimension == "Uniqueness":
        check_name = f"{field} UNIQUE"
        check_type = "unique"
        threshold = 0

    elif dimension == "Completeness":
        check_name = f"{field} NOT NULL"
        check_type = "not_null"
        threshold = 0

    elif dimension == "Validity":
        check_name = f"{field} valid"
        check_type = "validity"
        threshold = 0

    else:
        check_name = f"{field} {dimension.lower()} check"
        check_type = dimension.lower()
        threshold = 0

    severity = random.choices(
        SEVERITIES,
        weights=[25, 40, 25, 10],
        k=1
    )[0]

    return {
        "check_id": check_id,
        "asset_id": int(asset["asset_id"]),
        "dimension": dimension,
        "check_name": check_name,
        "check_type": check_type,
        "threshold": threshold,
        "severity": severity,
        "is_active": True,
        "created_at": datetime(
            2026, 1, ((check_id - 1) % 25) + 1,
            8, 0, 0, tzinfo=timezone.utc
        ).isoformat(),
    }


def main():
    random.seed(SEED + 4)

    with (Path(OUTPUT_DIR) / "data_assets.csv").open(encoding="utf-8") as f:
        assets = list(csv.DictReader(f))

    rows = []
    check_id = 1

    # ---------------------------------------------------------
    # 1. Create the four required incident checks first.
    # ---------------------------------------------------------
    for customer_id, asset_name, dimension in REQUIRED_CHECKS:

        matching_assets = [
            asset for asset in assets
            if int(asset["customer_id"]) == customer_id
            and asset["asset_name"] == asset_name
        ]

        if not matching_assets:
            raise ValueError(
                f"Required asset missing: "
                f"Customer {customer_id} / {asset_name}"
            )

        asset = matching_assets[0]

        rows.append(
            build_check(
                asset,
                dimension,
                check_id
            )
        )

        check_id += 1

    # ---------------------------------------------------------
    # 2. Generate normal checks for the remaining assets.
    # ---------------------------------------------------------
    for asset in assets:

        # 2–4 checks per normal asset,
        # 4–6 for critical assets.
        n_checks = (
            random.randint(4, 6)
            if asset["criticality"] == "Critical"
            else random.randint(2, 4)
        )

        dimensions = random.sample(
            QUALITY_DIMENSIONS,
            min(n_checks, len(QUALITY_DIMENSIONS))
        )

        for dimension in dimensions:

            # Avoid creating a duplicate required incident check.
            customer_id = int(asset["customer_id"])
            asset_name = asset["asset_name"]

            if (
                customer_id,
                asset_name,
                dimension
            ) in REQUIRED_CHECKS:
                continue

            rows.append(
                build_check(
                    asset,
                    dimension,
                    check_id
                )
            )

            check_id += 1

    # ---------------------------------------------------------
    # 3. Keep exactly the required number of checks.
    #
    #    Required incident checks are always preserved.
    # ---------------------------------------------------------
    target = COUNTS["checks"]

    required_rows = []
    normal_rows = []

    for row in rows:
        asset = next(
            a for a in assets
            if int(a["asset_id"]) == int(row["asset_id"])
        )

        key = (
            int(asset["customer_id"]),
            asset["asset_name"],
            row["dimension"]
        )

        if key in REQUIRED_CHECKS:
            required_rows.append(row)
        else:
            normal_rows.append(row)

    random.shuffle(normal_rows)

    remaining_slots = target - len(required_rows)

    if remaining_slots < 0:
        raise ValueError(
            "Number of required checks exceeds target check count."
        )

    rows = required_rows + normal_rows[:remaining_slots]

    # ---------------------------------------------------------
    # 4. If necessary, pad to exactly 450 checks.
    # ---------------------------------------------------------
    while len(rows) < target:

        asset = assets[(len(rows)) % len(assets)]

        rows.append({
            "check_id": len(rows) + 1,
            "asset_id": int(asset["asset_id"]),
            "dimension": "Completeness",
            "check_name": (
                f"{asset['asset_name']} record completeness"
            ),
            "check_type": "not_null",
            "threshold": 0,
            "severity": "Medium",
            "is_active": True,
            "created_at": datetime(
                2026, 1, 1, 8, 0, 0,
                tzinfo=timezone.utc
            ).isoformat(),
        })

    # ---------------------------------------------------------
    # 5. Re-number check IDs.
    # ---------------------------------------------------------
    for i, row in enumerate(rows, start=1):
        row["check_id"] = i

    path = Path(OUTPUT_DIR) / "quality_checks.csv"

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