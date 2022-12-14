from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, UniqueConstraint, Numeric, JSON, Date, PrimaryKeyConstraint
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String, ARRAY
from sqlalchemy.sql import func


Base = declarative_base()


class RawCustomer(Base):
    __tablename__ = "raw_customer"
    __table_args__ = (
        PrimaryKeyConstraint("id", "cut_off_date", name='pk_raw_customer_id'),
        UniqueConstraint("email_address", "cut_off_date", name='uk_raw_customer_email')
    )

    id = Column(Integer)
    email_address = Column(String(320), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    cut_off_date = Column(Date, nullable=False)
    inserted_datetime = Column(DateTime, server_default=func.now())


class DimCustomer(Base):
    __tablename__ = "dim_customer"
    __table_args__ = (
        UniqueConstraint("customer_sk", "valid_from", name='uk_dim_customer_id_ins'),
        UniqueConstraint("email_address", "valid_from", name='uk_dim_customer_email_ins'),
    )

    customer_pk = Column(Integer, primary_key=True)
    customer_sk = Column(Integer, nullable=False)
    customer_nk = Column(Integer, nullable=False)
    source_system = Column(String(5), nullable=False)
    email_address = Column(String(320), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    changed_fields = Column(ARRAY(String))
    valid_from = Column(DateTime)
    valid_to = Column(DateTime)
    inserted_datetime = Column(DateTime, server_default=func.now())
    updated_datetime = Column(DateTime, server_default=func.now())


class RawOrder(Base):
    __tablename__ = "raw_order"
    __table_args__ = (
        PrimaryKeyConstraint("id", "cut_off_date", name='uk_raw_order_id'),
    )

    id = Column(Integer)
    order_timestamp = Column(DateTime)
    customer_id = Column(Integer, nullable=False)
    order_status = Column(String(10), nullable=False)
    order_amount = Column(Numeric(10, 2), nullable=False)
    order_currency = Column(String(3), nullable=False)
    products = Column(JSON, nullable=False)
    cut_off_date = Column(Date, nullable=False)
    inserted_datetime = Column(DateTime, server_default=func.now())


class FactDailySales(Base):
    __tablename__ = "fact_daily_sales"
    __table_args__ = (
        PrimaryKeyConstraint("sales_date", "customer_pk", name='pk_fact_sales_cust_pk'),
        UniqueConstraint("sales_date", "customer_sk", name='uk_fact_sales_cust_sk'),
    )

    sales_date = Column(Date, nullable=False)
    customer_pk = Column(Integer, nullable=False)
    customer_sk = Column(Integer, nullable=False)
    sales_amount_eur = Column(Numeric(10, 2), nullable=False)
    number_of_products = Column(Integer, nullable=False)
    number_of_orders = Column(Integer, nullable=False)

    inserted_datetime = Column(DateTime, server_default=func.now())
