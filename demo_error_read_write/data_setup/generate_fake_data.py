from faker import Faker
import random
import pandas as pd
import os


def generate_random_customer(corrupted: bool = False):
    records = []
    faker = Faker()
    start = 1
    end = 10
    if corrupted:
        start = 8
        end = 12
    for i in range(start, end):
        records.append([
            random.choice(['a', 'b', 'c']) if corrupted and i % 2 else i,
            faker.email(),
            faker.first_name(),
            faker.last_name()
        ])
    df = pd.DataFrame(records, columns=['id', 'email_address', 'first_name', 'last_name'])
    return df


def generate_random_orders(corrupted: bool = False):
    records = []
    faker = Faker()
    start = 1
    end = 30
    if corrupted:
        start = 26
        end = 36
    for i in range(1, 30):
        records.append([
            random.choice(['a', 'b', 'c']) if corrupted and i % 2 else i,
            faker.date_time_between('-10d', '-1d').strftime("%Y-%m-%d %H:%M:%S"),
            random.randint(1, 11),
            random.choice(['NEW', 'DELIVERED']),
            random.randrange(10000) / 100,
            'EUR',
            [{'product_id': i, 'amount': random.randint(1, 3)}
                for i in random.sample(range(10, 30), random.randint(1, 4))]
        ])
    df = pd.DataFrame(records, columns=[
        'id', 'order_timestamp', 'customer_id', 'order_status', 'order_amount', 'order_currency', 'products'
    ])
    return df
