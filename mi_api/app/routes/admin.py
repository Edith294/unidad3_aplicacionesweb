from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/usuarios/<int:id>", methods=["DELETE"])
@jwt_required()
def eliminar_usuario(id):
    claims = get_jwt()
    if claims.get("rol") != "admin":
        return jsonify({"error": "Acceso denegado. Solo admins."}), 403
    return jsonify({"mensaje": f"Usuario {id} eliminado"}), 200
