from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.producto import Producto

productos_bp = Blueprint("productos", __name__)

@productos_bp.route("/", methods=["POST"])
@jwt_required()
def crear_producto():
    datos = request.get_json() or {}
    producto = Producto(
        sku=datos.get("sku"),
        nombre=datos.get("nombre"),
        precio=datos.get("precio", 0),
        stock=datos.get("stock", 0),
        categoria_id=datos.get("categoria_id", 1)
    )
    db.session.add(producto)
    db.session.commit()
    return jsonify({"producto": producto.to_dict()}), 201

@productos_bp.route("/", methods=["GET"])
def listar_productos():
    buscar = request.args.get("buscar", "")
    query = Producto.query.filter_by(activo=True)
    if buscar:
        query = query.filter(Producto.nombre.ilike(f"%{buscar}%"))
    productos = query.all()
    return jsonify({"productos": [p.to_dict() for p in productos]}), 200

@productos_bp.route("/<int:id>", methods=["GET"])
def obtener_producto(id):
    p = Producto.query.get(id)
    if not p:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify(p.to_dict()), 200
