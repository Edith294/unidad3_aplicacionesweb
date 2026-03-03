from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.materia import Materia

materias_bp = Blueprint("materias", __name__)

@materias_bp.route("/", methods=["POST"])
@jwt_required()
def crear_materia():
    datos = request.get_json() or {}
    materia = Materia(
        clave=datos.get("clave"),
        nombre=datos.get("nombre"),
        creditos=datos.get("creditos", 3),
        docente=datos.get("docente")
    )
    db.session.add(materia)
    db.session.commit()
    return jsonify({"materia": materia.to_dict()}), 201

@materias_bp.route("/", methods=["GET"])
def listar_materias():
    materias = Materia.query.filter_by(activa=True).all()
    return jsonify({"materias": [m.to_dict() for m in materias]}), 200
