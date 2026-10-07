{{ config(materialized='view') }}

SELECT
    source_id,
    customer_id,
    source_name,
    source_type,
    created_at,
    status
FROM {{ source('raw', 'data_sources') }}