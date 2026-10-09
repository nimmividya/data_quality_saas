{{ config(materialized='table') }}

SELECT
    a.customer_id,
    c.customer_name,
    COUNT(DISTINCT a.asset_id) AS total_assets,
    COUNT(DISTINCT a.pipeline_id) AS total_pipelines,
    COUNT(*) AS total_quality_results,
    SUM(
        CASE
            WHEN a.result_status = 'FAIL' THEN 1
            ELSE 0
        END
    ) AS failed_quality_results,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN a.result_status = 'PASS' THEN 1
                ELSE 0
            END
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS quality_pass_rate

FROM {{ ref('int_asset_quality') }} AS a

LEFT JOIN {{ ref('stg_customers') }} AS c
    ON a.customer_id = c.customer_id

GROUP BY
    a.customer_id,
    c.customer_name
