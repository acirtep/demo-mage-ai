select 
from (
select id, email_address, first_name, last_name
from postgres.raw_customer 
where cut_off_date='2022-11-16'
)