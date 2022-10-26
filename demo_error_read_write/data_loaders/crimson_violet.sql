select *
from raw_orders_pandas ord 
inner join raw_customers_pandas cust on (ord.customer_id = cust.id);