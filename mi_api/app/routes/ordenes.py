from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.orden import Orden
from app.models.producto import Producto

ordenes_bp = Blueprint("ordenes", __name__)

@ordenes_bp.route("/", methods=["POST"])
@jwt_required()
def crear_orden():
    datos = request.get_json() or {}
    productos_solicitados = datos.get("productos", [])

    if not productos_solicitados:
        return jsonify({"error": "Se requiere al menos un producto"}), 400

    total = 0
    items_validados = []

    for item in productos_solicitados:
        producto = Producto.query.get(item.get("producto_id"))
        if not producto:
            return jsonify({"error": f"Producto {item.get('producto_id')} no encontrado"}), 404

        cantidad = item.get("cantidad", 1)
        if producto.stock < cantidad:
            return jsonify({
                "error": f"Stock insuficiente para '{producto.nombre}'. "
                         f"Disponible: {producto.stock}, solicitado: {cantidad}"
            }), 400

        total += producto.precio * cantidad
        items_validados.append((producto, cantidad))

    # Todo válido: aplicar cambios
    for producto, cantidad in items_validados:
        producto.stock -= cantidad

    orden = Orden(cliente_id=datos.get("cliente_id", 1), total=total)
    db.session.add(orden)
    db.session.commit()

    return jsonify({
        "orden_id": orden.id,
        "total": total,
        "productos_comprados": len(items_validados),
        "estado": orden.estado
    }), 201
