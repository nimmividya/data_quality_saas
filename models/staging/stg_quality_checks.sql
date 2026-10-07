{{ config(materialized='view') }}

SELECT
    check_id,
    asset_id,
    dimension,
    check_name,
    check_type,
    threshold,
    severity,
    is_active,
    created_at
FROM {{ source('raw', 'quality_checks') }}