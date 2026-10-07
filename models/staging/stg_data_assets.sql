{{ config(materialized='view') }}

SELECT
    asset_id,
    customer_id,
    pipeline_id,
    asset_name,
    asset_type,
    criticality,
    expected_refresh_hours,
    status,
    created_at
FROM {{ source('raw', 'data_assets') }}