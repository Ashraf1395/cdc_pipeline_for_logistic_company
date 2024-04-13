from flask import Flask, render_template, request, jsonify
from flask_restful import Api, Resource, reqparse
import psycopg2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

api = Api(app)

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="metastore",
    user="hive",
    password="hive",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Helper function to execute SQL query
def execute_query(query, args=None):
    cur.execute(query, args)
    conn.commit()

# CRUD operations for customers
class Customers(Resource):
    def get(self):
        cur.execute("SELECT * FROM customers")
        customers = cur.fetchall()
        return jsonify(customers)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("customer_name", required=True)
        parser.add_argument("customer_address", required=True)
        # Add more arguments as needed
        args = parser.parse_args()

        query = "INSERT INTO customers (customer_name, customer_address) VALUES (%s, %s)"
        execute_query(query, (args["customer_name"], args["customer_address"]))

        return jsonify({"message": "Customer added successfully"}), 201

    def put(self, customer_id):
        parser = reqparse.RequestParser()
        parser.add_argument("customer_name", required=True)
        parser.add_argument("customer_address", required=True)
        # Add more arguments as needed
        args = parser.parse_args()

        query = "UPDATE customers SET customer_name = %s, customer_address = %s WHERE customer_id = %s"
        execute_query(query, (args["customer_name"], args["customer_address"], customer_id))

        return jsonify({"message": "Customer updated successfully"})

    def delete(self, customer_id):
        query = "DELETE FROM customers WHERE customer_id = %s"
        execute_query(query, (customer_id,))
        return jsonify({"message": "Customer deleted successfully"})

api.add_resource(Customers, "/api/customers", "/api/customers/<string:customer_id>")

# CRUD operations for drivers
class Drivers(Resource):
    def get(self):
        cur.execute("SELECT * FROM drivers")
        drivers = cur.fetchall()
        return jsonify(drivers)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("driver_name", required=True)
        parser.add_argument("driver_address", required=True)
        # Add more arguments as needed
        args = parser.parse_args()

        query = "INSERT INTO drivers (driver_name, driver_address) VALUES (%s, %s)"
        execute_query(query, (args["driver_name"], args["driver_address"]))

        return jsonify({"message": "Driver added successfully"}), 201

    def put(self, driver_id):
        parser = reqparse.RequestParser()
        parser.add_argument("driver_name", required=True)
        parser.add_argument("driver_address", required=True)
        # Add more arguments as needed
        args = parser.parse_args()

        query = "UPDATE drivers SET driver_name = %s, driver_address = %s WHERE driver_id = %s"
        execute_query(query, (args["driver_name"], args["driver_address"], driver_id))

        return jsonify({"message": "Driver updated successfully"})

    def delete(self, driver_id):
        query = "DELETE FROM drivers WHERE driver_id = %s"
        execute_query(query, (driver_id,))
        return jsonify({"message": "Driver deleted successfully"})

api.add_resource(Drivers, "/api/drivers", "/api/drivers/<string:driver_id>")

# CRUD operations for orders
class Orders(Resource):
    def get(self):
        cur.execute("SELECT * FROM orders")
        orders = cur.fetchall()
        return jsonify(orders)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("order_name", required=True)
        parser.add_argument("order_address", required=True)
        # Add more arguments as needed
        args = parser.parse_args()

        query = "INSERT INTO orders (order_name, order_address) VALUES (%s, %s)"
        execute_query(query, (args["order_name"], args["order_address"]))

        return jsonify({"message": "Order added successfully"}), 201

    def put(self, order_id):
        parser = reqparse.RequestParser()
        parser.add_argument("order_name", required=True)
        parser.add_argument("order_address", required=True)
        # Add more arguments as needed
        args = parser.parse_args()

        query = "UPDATE orders SET order_name = %s, order_address = %s WHERE order_id = %s"
        execute_query(query, (args["order_name"], args["order_address"], order_id))

        return jsonify({"message": "Order updated successfully"})

    def delete(self, order_id):
        query = "DELETE FROM orders WHERE order_id = %s"
        execute_query(query, (order_id,))
        return jsonify({"message": "Order deleted successfully"})

api.add_resource(Orders, "/api/orders", "/api/orders/<string:order_id>")

# CRUD operations for assignments
class Assignments(Resource):
    def get(self):
        cur.execute("SELECT * FROM assignments")
        assignments = cur.fetchall()
        return jsonify(assignments)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("assignment_name", required=True)
        parser.add_argument("assignment_address", required=True)
        # Add more arguments as needed
        args = parser.parse_args()

        query = "INSERT INTO assignments (assignment_name, assignment_address) VALUES (%s, %s)"
        execute_query(query, (args["assignment_name"], args["assignment_address"]))

        return jsonify({"message": "Assignment added successfully"}), 201

    def put(self, assignment_id):
        parser = reqparse.RequestParser()
        parser.add_argument("assignment_name", required=True)
        parser.add_argument("assignment_address", required=True)
        # Add more arguments as needed
        args = parser.parse_args()

        query = "UPDATE assignments SET assignment_name = %s, assignment_address = %s WHERE assignment_id = %s"
        execute_query(query, (args["assignment_name"], args["assignment_address"], assignment_id))

        return jsonify({"message": "Assignment updated successfully"})

    def delete(self, assignment_id):
        query = "DELETE FROM assignments WHERE assignment_id = %s"
        execute_query(query, (assignment_id,))
        return jsonify({"message": "Assignment deleted successfully"})

api.add_resource(Assignments, "/api/assignments", "/api/assignments/<string:assignment_id>")

@app.route('/customers')
def customers_page():
    return render_template('customers.html')

# Render add_customer.html template
@app.route('/add_customer')
def add_customer_page():
    return render_template('add_customer.html')

@app.route('/orders')
def orders_page():
    return render_template('orders.html')

# Render add_order.html template
@app.route('/add_order')
def add_order_page():
    return render_template('add_order.html')

@app.route('/drivers')
def drivers_page():
    return render_template('drivers.html')

# Render add_driver.html template
@app.route('/add_driver')
def add_driver_page():
    return render_template('add_driver.html')

@app.route('/assignments')
def assignments_page():
    return render_template('assignments.html')

# Render add_assignment.html template
@app.route('/add_assignment')
def add_assignment_page():
    return render_template('add_assignment.html')

# Route to serve nav.html
@app.route('/nav.html')
def nav():
    return app.send_static_file('nav.html')

if __name__ == '__main__':
    app.run(debug=True)
