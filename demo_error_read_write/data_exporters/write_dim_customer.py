from pandas import DataFrame
from sqlalchemy import create_engine
from datetime import datetime, timedelta

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(df=None, **kwargs):
    """
    Exports data to some source

    Args:
        df (DataFrame): Data frame to export to

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    # Specify your data exporting logic here
    cut_off_date = kwargs["cut_off_date"]
    cut_off_date_yday = datetime.strptime(cut_off_date, '%Y-%m-%d') - timedelta(days=1)
    cut_off_date_yday = cut_off_date_yday.date()

    conn = create_engine("postgresql://postgres:postgres@postgres_db:5432/postgres")
    with conn.begin() as conn:
        conn.execute(r"""
        MERGE into dim_customer tgt
        using (
        select
            rc.id as customer_sk,
            rc.id as customer_nk,
            'ONE' as source_system,
            rc.email_address,
            rc.first_name,
            rc.last_name,
            rc.cut_off_date as valid_from,
            '9999-12-31'::date as valid_to,
            null as changed_fields
        from raw_customer rc
        left join dim_customer dc on (
            rc.id = dc.customer_nk and dc.valid_to='9999-12-31')
        where rc.cut_off_date='{cut_off_date}'
        and dc.customer_pk is null
        union all
            select
            rc.id as customer_sk,
            rc.id as customer_nk,
            'ONE' as source_system,
            rc.email_address,
            rc.first_name,
            rc.last_name,
            rc.cut_off_date as valid_from,
            '9999-12-31'::date as valid_to,
            array[case when rc.email_address <> dc.email_address then 'email_address'
            end, case when rc.first_name <> dc.first_name then 'first_name' end,
            case when rc.last_name <> dc.last_name then 'last_name' end] as changed_fields
        from raw_customer rc
        inner join dim_customer dc on (
            rc.id = dc.customer_nk)
        where rc.cut_off_date='{cut_off_date}'
        and dc.valid_to='9999-12-31'
        and array[rc.email_address, rc.first_name, rc.last_name] <> array[dc.email_address, dc.first_name, dc.last_name]
        ) src
        on (tgt.customer_sk = src.customer_sk and tgt.valid_to='9999-12-31')
        when matched then update set valid_to = '{cut_off_date_yday}', updated_datetime= current_timestamp, changed_fields=src.changed_fields
        when not matched then
        insert (customer_sk, customer_nk, source_system, email_address, first_name, last_name, valid_from, valid_to)
        Values (src.customer_sk, src.customer_nk, src.source_system, src.email_address, src.first_name, src.last_name, src.valid_from, src.valid_to)
            """.format(cut_off_date=cut_off_date, cut_off_date_yday=cut_off_date_yday))
        

