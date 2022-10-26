create table raw_customers_managed(
        id integer primary key,
        email_address varchar(320) not null unique,
        first_name varchar(100),     
        last_name varchar(100),
        inserted_datetime timestamp not null default current_timestamp 
    );
