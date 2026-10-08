{{ config(
    materialized='table'
) }}

with pipeline_runs as (select pipeline_id,
                              pipeline_name,
                              customer_id,
                              run_id,
                              started_at,
                              run_status,
                              run_duration_minutes
                       from {{ ref('int_pipeline_run_quality') }}),

     pipeline_summary as (select pipeline_id,
                                 pipeline_name,
                                 customer_id,

                                 count(*)                           as total_runs,

                                 count_if(run_status = 'Failed')    as failed_runs,

                                 count_if(run_status = 'Succeeded') as successful_runs,

                                 round(
                                         100.0 * count_if(run_status = 'Succeeded') / nullif(count(*), 0), 2
                                 )                                  as pipeline_success_rate,

                                 round(
                                         avg(run_duration_minutes),
                                         2
                                 )                                  as avg_run_duration_minutes,

                                 round(
                                         max(run_duration_minutes),
                                         2
                                 )                                  as max_run_duration_minutes

                          from pipeline_runs

                          group by pipeline_id,
                                   pipeline_name,
                                   customer_id)

select *
from pipeline_summary
order by pipeline_success_rate asc,
         failed_runs desc