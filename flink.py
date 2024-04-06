from pyflink.table import EnvironmentSettings,TableEnvironment
import os

#Create a batch TableEnvironment
env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)


# Get the current working directory
CURRENT_DIR = os.getcwd()

# Define a list of JAR file names you want to add
jar_files = [
    "flink-sql-connector-postgres-cdc-2.4.1.jar",
    "postgresql-42.6.0.jar",
    "flink-connector-jdbc-1.16.1.jar", 
]

# Build the list of JAR URLs by prepending 'file:///' to each file name
jar_urls = [f"file:///{CURRENT_DIR}/jar-files/{jar_file}" for jar_file in jar_files]

table_env.get_config().get_configuration().set_string(
    "pipeline.jars",
    ";".join(jar_urls)
)

table_env.get_config().get_configuration().set_string(
    "execution.checkpointing.interval",
    "5000"
)

table_env.get_config().get_configuration().set_string(
    "parallelism.default",
    "4"
)

# Configure checkpointing
table_env.get_config().get_configuration().set_string(
    "execution.checkpointing.mode",
    "EXACTLY_ONCE"
)

# Set the checkpointing directory to the current directory
table_env.get_config().get_configuration().set_string(
    "execution.checkpointing.checkpoints-directory",
    CURRENT_DIR
)



# Create a source for the "customer_source" table
customer_source = f"""
CREATE TABLE IF NOT EXISTS customer_source (
    customer_id INT,
    name STRING,
    city STRING,
    state STRING,
    db_name STRING METADATA FROM 'database_name' VIRTUAL,
    table_name STRING METADATA  FROM 'table_name' VIRTUAL,
    operation_ts TIMESTAMP_LTZ(3) METADATA FROM 'op_ts' VIRTUAL,
    PRIMARY KEY (customer_id) NOT ENFORCED
 ) WITH (
   'connector' = 'postgres-cdc',
   'hostname' = 'localhost',
   'port' = '5432',
   'username' = 'root',
   'password' = 'ashraf',
   'database-name' = 'truck_delivery_data',
   'schema-name' = 'public',
   'slot.name' = 'customer_slot',
   'decoding.plugin.name' = 'pgoutput',
   'scan.incremental.snapshot.enabled' = 'true',
   'table-name' = 'customers'
 );
"""

# Create a source for the "order_source" table
order_source = f"""
CREATE TABLE IF NOT EXISTS order_source (
    order_id INT,
    order_value DOUBLE PRECISION,
    customer_id INT,
    db_name STRING METADATA FROM 'database_name' VIRTUAL,
    table_name STRING METADATA  FROM 'table_name' VIRTUAL,
    operation_ts TIMESTAMP_LTZ(3) METADATA FROM 'op_ts' VIRTUAL,
    PRIMARY KEY (order_id) NOT ENFORCED
 ) WITH (
   'connector' = 'postgres-cdc',
   'hostname' = 'localhost',
   'port' = '5432',
   'username' = 'root',
   'password' = 'ashraf',
   'database-name' = 'truck_delivery_data',
   'schema-name' = 'public',
   'slot.name' = 'order_slot',
   'decoding.plugin.name' = 'pgoutput',
    'scan.incremental.snapshot.enabled' = 'true',
   'table-name' = 'orders'
 );
"""
# Execute the SQL to create the sources
table_env.execute_sql(customer_source)
table_env.execute_sql(order_source)

print("Created customer_source and order_source tables.")
print("Created order_source and order_source tables.")


# table_env.execute_sql("""
#     SELECT DISTINCT
#       CAST(o.order_id AS STRING) AS order_id,
#       CAST(o.operation_ts AS STRING) AS operation_ts,
#       CAST(c.name AS STRING) AS customer_name,
#       CAST(c.city AS STRING) AS customer_city,
#       CAST(c.state AS STRING) AS customer_state,
#       CAST(o.order_value AS STRING) AS price
#     FROM
#       customer_source AS c
#     INNER JOIN
#       order_source AS o
#     ON
#       c.customer_id = o.customer_id;
# """).print()




# print("Job started.")

# Define the JDBC sink table schema to match the query result schema
jdbc_sink = """
CREATE TABLE order_enriched_jdbc_sink (
   order_id STRING,
   operation_ts STRING,
   customer_name STRING,
   customer_city STRING,
   customer_state STRING,
   price STRING,
   PRIMARY KEY (order_id) NOT ENFORCED
 )
 WITH (
   'connector' = 'jdbc',  -- Use JDBC connector
   'url' = 'jdbc:postgresql://localhost:5432/truck_delivery_data', 
   'table-name' = 'order_enriched', 
   'driver' = 'org.postgresql.Driver',
   'username' = 'root', 
   'password' = 'ashraf', 
   'sink.buffer-flush.max-rows' = '1000',  -- Adjust batch size as needed
   'sink.buffer-flush.interval' = '2s'  -- Adjust flush interval as needed
 );
"""

# Execute the SQL to create the JDBC sink table
table_env.execute_sql(jdbc_sink)


print('Here')
table_env.execute_sql("""
    INSERT INTO order_enriched_jdbc_sink
    SELECT DISTINCT
      CAST(o.order_id AS STRING) AS order_id,
      CAST(o.operation_ts AS STRING) AS operation_ts,
      CAST(c.name AS STRING) AS customer_name,
      CAST(c.city AS STRING) AS customer_city,
      CAST(c.state AS STRING) AS customer_state,
      CAST(o.order_value AS STRING) AS price
    FROM
      customer_source AS c
    INNER JOIN
      order_source AS o
    ON
      c.customer_id = o.customer_id;
""").wait()

print("Job started.")