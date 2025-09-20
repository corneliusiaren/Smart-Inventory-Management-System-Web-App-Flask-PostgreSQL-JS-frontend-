from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL','postgresql://postgres:password@localhost/inventory')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    sku = db.Column(db.String, unique=True)
    quantity = db.Column(db.Integer, default=0)
    reorder_level = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/items', methods=['GET','POST'])
def items():
    if request.method == 'GET':
        items = Item.query.all()
        return jsonify([{'id':i.id,'name':i.name,'sku':i.sku,'quantity':i.quantity,'reorder_level':i.reorder_level} for i in items])
    data = request.get_json()
    item = Item(name=data['name'], sku=data.get('sku'), quantity=data.get('quantity',0), reorder_level=data.get('reorder_level',10))
    db.session.add(item); db.session.commit()
    return jsonify({'id': item.id}), 201

@app.route('/api/items/<int:item_id>/adjust', methods=['POST'])
def adjust(item_id):
    data = request.get_json()
    delta = int(data.get('change',0))
    item = Item.query.get_or_404(item_id)
    item.quantity += delta
    db.session.commit()
    return jsonify({'id': item.id, 'quantity': item.quantity})

if __name__ == '__main__':
    app.run(debug=True)
