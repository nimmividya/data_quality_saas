{{ config(materialized='view') }}

SELECT
    result_id,
    check_id,
    run_time,
    status,
    records_checked,
    failed_records,
    failure_rate,
    execution_duration_ms
FROM {{ source('raw', 'quality_results') }}