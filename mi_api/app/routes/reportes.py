from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.models.orden import Orden
from app.models.producto import Producto

reportes_bp = Blueprint("reportes", __name__)

@reportes_bp.route("/ventas", methods=["GET"])
@jwt_required()
def reporte_ventas():
    claims = get_jwt()
    if claims.get("rol") != "admin":
        return jsonify({"error": "Acceso denegado. Solo admins."}), 403

    ordenes = Orden.query.all()
    total_ingresos = sum(o.total for o in ordenes)

    productos = Producto.query.all()
    top_productos = sorted(productos, key=lambda p: p.stock)[:5]

    return jsonify({
        "resumen": {
            "total_ordenes": len(ordenes),
            "ingresos": total_ingresos
        },
        "top_productos": [p.to_dict() for p in top_productos]
    }), 200
