{{ config(materialized='view') }}

SELECT
    run_id,
    pipeline_id,
    started_at,
    completed_at,
    status,
    records_processed,
    error_message
FROM {{ source('raw', 'pipeline_runs') }}