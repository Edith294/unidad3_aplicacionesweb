from flask import Blueprint, request, jsonify
from app import db
from app.models.calificacion import Calificacion

calificaciones_bp = Blueprint("calificaciones", __name__)

@calificaciones_bp.route("/", methods=["POST"])
def registrar_calificacion():
    datos = request.get_json() or {}

    campos = ["estudiante_id", "materia_id", "calificacion"]
    for c in campos:
        if c not in datos:
            return jsonify({"error": f"Falta el campo '{c}'"}), 400

    cal = datos["calificacion"]
    if not (0 <= cal <= 100):
        return jsonify({"error": "La calificación debe estar entre 0 y 100"}), 400

    nueva = Calificacion(
        estudiante_id=datos["estudiante_id"],
        materia_id=datos["materia_id"],
        calificacion=cal,
        periodo=datos.get("periodo", "2024-1")
    )
    db.session.add(nueva)
    db.session.commit()

    result = nueva.to_dict()
    return jsonify(result), 201
