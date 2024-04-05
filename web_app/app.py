from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# POSTGRES_DBNAME=truck_delivery_data
# POSTGRES_SCHEMA=public
# POSTGRES_USER=root
# POSTGRES_PASSWORD=ashraf
# POSTGRES_HOST=postgres
# POSTGRES_PORT=5432

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:ashraf@localhost/truck_delivery_data'
db = SQLAlchemy(app)


class TruckData(db.Model):
    __tablename__ = 'truck_data'

    id = db.Column(db.Integer, primary_key=True)
    GpsProvider = db.Column(db.String())
    BookingID = db.Column(db.String())
    # Add other columns here

    def __repr__(self):
        return f'<TruckData {self.id}>'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/trucks', methods=['GET', 'POST'])
def trucks():
    if request.method == 'GET':
        # Fetch all truck data
        trucks = TruckData.query.all()
        return render_template('trucks.html', trucks=trucks)
    elif request.method == 'POST':
        # Create a new truck entry
        data = request.json
        new_truck = TruckData(**data)
        db.session.add(new_truck)
        db.session.commit()
        return jsonify({'message': 'Truck data added successfully'})

@app.route('/trucks/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def truck_detail(id):
    truck = TruckData.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify(truck)
    elif request.method == 'PUT':
        data = request.json
        # Update truck data
        # Example: truck.GpsProvider = data['GpsProvider']
        db.session.commit()
        return jsonify({'message': 'Truck data updated successfully'})
    elif request.method == 'DELETE':
        db.session.delete(truck)
        db.session.commit()
        return jsonify({'message': 'Truck data deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
