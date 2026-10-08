{{ config(materialized='view') }}

SELECT
    r.run_id,
    r.pipeline_id,
    p.pipeline_name,
    p.source_id,
    s.source_name,
    s.customer_id,
    r.started_at,
    r.completed_at,
    r.status AS run_status,
    r.records_processed,
    r.error_message,
    p.schedule,
    p.expected_frequency_minutes,
    p.status AS pipeline_status,
    s.status AS source_status,
    DATEDIFF(
        'minute',
        r.started_at,
        r.completed_at
    ) AS run_duration_minutes
FROM {{ ref('stg_pipeline_runs') }} AS r
LEFT JOIN {{ ref('stg_pipelines') }} AS p
    ON r.pipeline_id = p.pipeline_id
LEFT JOIN {{ ref('stg_data_sources') }} AS s
    ON p.source_id = s.source_id
