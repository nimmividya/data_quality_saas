{{ config(materialized='view') }}

SELECT
    pipeline_id,
    source_id,
    pipeline_name,
    schedule,
    expected_frequency_minutes,
    status,
    created_at
FROM {{ source('raw', 'pipelines') }}