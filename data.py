from faker import Faker
import pandas as pd
import random
from datetime import datetime
fake = Faker()

def generate_customer_data(num_customers):
    customers = []
    for _ in range(num_customers):
        customer = {
            'customer_id': fake.uuid4(),
            'customer_name': fake.name(),
            'customer_address': fake.street_address(),
            'customer_city': fake.city(),
            'customer_state': fake.state(),
            'customer_zip_code': fake.zipcode(),
            'customer_contact_number': fake.phone_number(),
            'customer_email': fake.email(),
            "ts": str(datetime.now().timestamp())
        }
        customers.append(customer)
    return customers

def generate_order_data(num_orders, customers):
    orders = []
    for _ in range(num_orders):
        customer = random.choice(customers)
        order = {
            'order_id': str(fake.uuid4()),  # Avro does not support UUID directly, so convert to string
            'customer_id': str(customer['customer_id']),  # Convert to string
            'order_date': fake.date_time_between(start_date='-30d', end_date='now').strftime('%Y-%m-%d %H:%M:%S'),
            'delivery_date': fake.date_time_between(start_date='now', end_date='+30d').strftime('%Y-%m-%d %H:%M:%S'),
            'order_status': random.choice(['Pending', 'In Progress', 'Completed']),
            'order_address': fake.street_address(),
            'order_city': fake.city(),
            'order_state': fake.state(),
            'order_zip_code': fake.zipcode(),
            'item_description': fake.word(),
            'item_quantity': random.randint(1, 10),
            'item_weight': round(random.uniform(0.1, 10.0), 2)  # Round to 2 decimal places for Avro compatibility
        }
        orders.append(order)
    return orders

def generate_driver_data(num_drivers):
    drivers = []
    for _ in range(num_drivers):
        driver = {
            'driver_id': str(fake.uuid4()),  # Convert to string
            'driver_name': fake.name(),
            'driver_contact_number': fake.phone_number(),
            'driver_license_number': str(fake.random_number(digits=10)),  # Convert to string
            'vehicle_id': str(fake.random_number(digits=6)),  # Convert to string
            'vehicle_type': random.choice(['Car', 'Truck', 'Van']),
            'vehicle_registration_number': str(fake.random_number(digits=8)),  # Convert to string
            'driver_status': random.choice(['Available', 'Busy', 'Offline']),
            'current_location_latitude': round(fake.latitude(), 6),  # Round to 6 decimal places for Avro compatibility
            'current_location_longitude': round(fake.longitude(), 6),  # Round to 6 decimal places for Avro compatibility
            "ts": str(datetime.now().timestamp())
        }
        drivers.append(driver)
    return drivers

def generate_assignment_data(num_assignments, orders, drivers):
    assignments = []
    for _ in range(num_assignments):
        order = random.choice(orders)
        driver = random.choice(drivers)
        assignment = {
            'assignment_id': str(fake.uuid4()),  # Convert to string
            'order_id': str(order['order_id']),  # Convert to string
            'driver_id': str(driver['driver_id']),  # Convert to string
            'assigned_date': fake.date_time_between(start_date='-1d', end_date='now').strftime('%Y-%m-%d %H:%M:%S'),
            'assigned_status': random.choice(['Pending', 'In Progress', 'Completed']),
            'assigned_address': order['order_address'],
            'assigned_city': order['order_city'],
            'assigned_state': order['order_state'],
            'assigned_zip_code': order['order_zip_code']
        }
        assignments.append(assignment)
    return assignments

# Generate fake data
num_customers = 10
num_orders = 20
num_drivers = 5
num_assignments = 15

customers = generate_customer_data(num_customers)
orders = generate_order_data(num_orders, customers)
drivers = generate_driver_data(num_drivers)
assignments = generate_assignment_data(num_assignments, orders, drivers)

# Create DataFrames
customers_df = pd.DataFrame(customers)
orders_df = pd.DataFrame(orders)
drivers_df = pd.DataFrame(drivers)
assignments_df = pd.DataFrame(assignments)

orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
orders_df['delivery_date'] = pd.to_datetime(orders_df['delivery_date'])
assignments_df['assigned_date'] = pd.to_datetime(assignments_df['assigned_date'])
print(orders_df.dtypes)
# Save DataFrames to CSV files
customers_df.to_csv('data/customers.csv', index=False)
orders_df.to_csv('data/orders.csv', index=False)
drivers_df.to_csv('data/drivers.csv', index=False)
assignments_df.to_csv('data/assignments.csv', index=False)


import psycopg2
from psycopg2 import sql
import pandas as pd

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="metastore",
    user="hive",
    password="hive",
    host="localhost",
    port="5432"
)

# Create a cursor object
cur = conn.cursor()


def import_csv_to_postgres(csv_file, df, table_name):
    
    # Drop existing table if it exists
    drop_table_query = sql.SQL('DROP TABLE IF EXISTS {}').format(sql.Identifier(table_name))
    cur.execute(drop_table_query)
    print(df.dtypes)   
    # Infer data types for each column
    
    dtypes=df.dtypes
    # Map pandas data types to PostgreSQL data types
    postgres_dtypes = {
        'object': 'VARCHAR',
        'int64': 'BIGINT',
        'float64': 'DOUBLE PRECISION',
        'bool': 'BOOLEAN',
        'datetime64[ns]': 'TIMESTAMP',
    }
    
    # Create table in PostgreSQL
    create_table_query = sql.SQL('''
        CREATE TABLE IF NOT EXISTS {} (
            {}
        )
    ''').format(
        sql.Identifier(table_name),
        sql.SQL(', ').join(
            sql.SQL(column.lower()) + sql.SQL(' ') + sql.SQL(postgres_dtypes[str(dtypes[column])]) for column in df.columns
        )
    )
    cur.execute(create_table_query)

    # Import data into PostgreSQL
    with open(csv_file, 'r') as f:
        next(f)  # Skip the header
        cur.copy_from(f, table_name, sep=',')
    
    conn.commit()
    print(f"Data imported into PostgreSQL table '{table_name}'.")

# Import data into PostgreSQL tables
import_csv_to_postgres('data/customers.csv',customers_df, 'customers')
import_csv_to_postgres('data/orders.csv',orders_df, 'orders')
import_csv_to_postgres('data/drivers.csv',drivers_df, 'drivers')
import_csv_to_postgres('data/assignments.csv',assignments_df, 'assignments')
# Close the cursor and connection
cur.close()
conn.close()
