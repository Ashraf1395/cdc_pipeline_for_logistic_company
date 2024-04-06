-- Create the "customers" table if it does not exist
CREATE TABLE IF NOT EXISTS public.customers (
  customer_id INT PRIMARY KEY,
  name TEXT,
  city TEXT,
  state TEXT
);

-- Create the "orders" table if it does not exist
CREATE TABLE IF NOT EXISTS public.orders (
  order_id INT PRIMARY KEY,
  order_value DOUBLE PRECISION,
  customer_id INT
);

-- Insert data into the "customers" table in the public schema
INSERT INTO public.customers (customer_id, name, city, state)
VALUES
  (1, 'Alice', 'New York', 'NY'),
  (2, 'Bob', 'Los Angeles', 'CA'),
  (3, 'Charlie', 'Chicago', 'IL');

-- Insert data into the "orders" table in the public schema
INSERT INTO public.orders (order_id, order_value, customer_id)
VALUES
  (101, 100.50, 1),
  (102, 75.25, 2),
  (103, 200.75, 1);

-- Enable full replica identity for the "customers" table
ALTER TABLE public.customers REPLICA IDENTITY FULL;

-- Enable full replica identity for the "orders" table
ALTER TABLE public.orders REPLICA IDENTITY FULL;

ALTER SYSTEM SET wal_level = 'logical';

-- DROP TABLE IF EXISTS public.order_enriched;

CREATE TABLE IF NOT EXISTS public.order_enriched
(
    order_id character varying(255) COLLATE pg_catalog."default" NOT NULL,
    operation_ts character varying(255) COLLATE pg_catalog."default",
    customer_name character varying(255) COLLATE pg_catalog."default",
    customer_city character varying(255) COLLATE pg_catalog."default",
    customer_state character varying(255) COLLATE pg_catalog."default",
    price character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT order_enriched_pkey PRIMARY KEY (order_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.order_enriched
    OWNER to truck_delivery_data;