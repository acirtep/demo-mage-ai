{% snapshot dim_customer_dbt %}

    {{
        config(
          target_schema='public',
          strategy='check',
          unique_key='customer_nk',
          updated_at='cut_off_date',
          check_cols=['email_address', 'first_name', 'last_name'],
        )
    }}

    select id as customer_nk,
           'ONE' as source_system,
           id as customer_sk,
           email_address,
           first_name,
           last_name,
           cut_off_date
    from raw_customers_pandas

{% endsnapshot %}