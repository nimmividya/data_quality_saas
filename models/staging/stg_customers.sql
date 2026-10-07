{{ config(materialized='view') }}

SELECT
    customer_id,
    customer_name,
    plan,
    status,
    created_at,
    profile
FROM {{ source('raw', 'customers') }}
