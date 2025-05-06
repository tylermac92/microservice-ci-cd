from flask import Blueprint, jsonify, request
from .models import Item, db
from flask_jwt_extended import jwt_required

bp = Blueprint('api', __name__)

@bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

@bp.route('/items', methods=['GET', 'POST', 'OPTIONS'])
@jwt_required()
def items():
    if request.method == 'OPTIONS':
        return '', 204

    if request.method == 'GET':
        items = Item.query.all()
        return jsonify([{'id': i.id, 'name': i.name} for i in items])

    if request.method == 'POST':
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'error': 'Missing item name'}), 400

        item = Item(name=data['name'])
        db.session.add(item)
        db.session.commit()
        return jsonify({'id': item.id, 'name': item.name}), 201


@bp.route('/items/<int:item_id>', methods=['PUT', 'DELETE', 'OPTIONS'])
@jwt_required()
def update_or_delete_item(item_id):
    if request.method == 'OPTIONS':
        return '', 204

    item = Item.query.get_or_404(item_id)

    if request.method == 'PUT':
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'error': 'Missing item name'}), 400

        item.name = data['name']
        db.session.commit()
        return jsonify({'id': item.id, 'name': item.name})

    if request.method == 'DELETE':
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted'})

print(">>> routes.py loaded")
