{{ config(materialized='view') }}

with source as (
    select * from {{ source('raw_api', 'raw_data') }}
)

select
    id as user_id,
    encrypted_content,
    cast(created_at as timestamp) as loaded_at
from source
