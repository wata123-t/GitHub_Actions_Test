{{ config(materialized='table') }}

select
    date(loaded_at) as event_date,
    count(user_id) as record_count
from {{ ref('stg_api_data') }}
group by 1
