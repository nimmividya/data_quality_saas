{{ config(materialized='view') }}

SELECT
    r.result_id,
    r.check_id,

    a.asset_id,
    a.customer_id,
    a.pipeline_id,
    a.asset_name,
    a.asset_type,
    a.criticality,

    c.dimension,
    c.check_name,
    c.check_type,
    c.threshold,
    c.severity,
    c.is_active,

    r.run_time,
    r.status AS result_status,
    r.records_checked,
    r.failed_records,
    r.failure_rate,
    r.execution_duration_ms

FROM {{ ref('stg_quality_results') }} AS r

LEFT JOIN {{ ref('stg_quality_checks') }} AS c
    ON r.check_id = c.check_id

LEFT JOIN {{ ref('stg_data_assets') }} AS a
    ON c.asset_id = a.asset_id