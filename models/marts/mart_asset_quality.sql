{{ config(materialized='table') }}

SELECT
    asset_id,
    asset_name,
    customer_id,
    pipeline_id,
    asset_type,
    criticality,

    COUNT(*) AS total_quality_results,

    SUM(
        CASE
            WHEN result_status = 'FAIL' THEN 1
            ELSE 0
        END
    ) AS failed_quality_results,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN result_status = 'PASS' THEN 1
                ELSE 0
            END
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS quality_pass_rate,

    SUM(failed_records) AS total_failed_records,

    ROUND(AVG(failure_rate), 4) AS avg_failure_rate,

    ROUND(MAX(failure_rate), 4) AS max_failure_rate,

    COUNT(
        DISTINCT CASE
            WHEN result_status = 'FAIL' THEN dimension
        END
    ) AS failed_dimensions

FROM {{ ref('int_asset_quality') }}

GROUP BY
    asset_id,
    asset_name,
    customer_id,
    pipeline_id,
    asset_type,
    criticality