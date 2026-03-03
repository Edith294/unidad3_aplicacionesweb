from flask import Blueprint, request, jsonify
from app import db
from app.models.estudiante import Estudiante

estudiantes_bp = Blueprint("estudiantes", __name__)

@estudiantes_bp.route("/", methods=["GET"])
def listar_estudiantes():
    pagina = request.args.get("pagina", 1, type=int)
    por_pagina = request.args.get("por_pagina", 10, type=int)

    query = Estudiante.query.filter_by(activo=True)
    paginacion = query.paginate(page=pagina, per_page=por_pagina, error_out=False)

    return jsonify({
        "estudiantes": [e.to_dict() for e in paginacion.items],
        "total": paginacion.total,
        "paginas": paginacion.pages,
        "pagina_actual": pagina
    }), 200

@estudiantes_bp.route("/<int:id>", methods=["GET"])
def obtener_estudiante(id):
    est = Estudiante.query.get(id)
    if not est or not est.activo:
        return jsonify({"error": "Estudiante no encontrado"}), 404
    return jsonify(est.to_dict()), 200

@estudiantes_bp.route("/", methods=["POST"])
def crear_estudiante():
    datos = request.get_json(silent=True)
    if not datos:
        return jsonify({"error": "Se requiere un body JSON válido"}), 400

    campos_requeridos = ["matricula", "nombre", "apellido", "email", "carrera"]
    for campo in campos_requeridos:
        if campo not in datos:
            return jsonify({"error": f"El campo '{campo}' es requerido"}), 400

    if Estudiante.query.filter_by(matricula=datos["matricula"]).first():
        return jsonify({"error": "La matrícula ya existe"}), 409

    if Estudiante.query.filter_by(email=datos["email"]).first():
        return jsonify({"error": "El email ya está registrado"}), 409

    est = Estudiante(**datos)
    db.session.add(est)
    db.session.commit()

    return jsonify({"mensaje": "Estudiante creado", "estudiante": est.to_dict()}), 201

@estudiantes_bp.route("/<int:id>", methods=["PUT"])
def actualizar_estudiante(id):
    est = Estudiante.query.get(id)
    if not est or not est.activo:
        return jsonify({"error": "Estudiante no encontrado"}), 404

    datos = request.get_json() or {}
    for campo, valor in datos.items():
        if hasattr(est, campo):
            setattr(est, campo, valor)

    db.session.commit()
    return jsonify({"mensaje": "Estudiante actualizado", "estudiante": est.to_dict()}), 200

@estudiantes_bp.route("/<int:id>", methods=["DELETE"])
def eliminar_estudiante(id):
    est = Estudiante.query.get(id)
    if not est:
        return jsonify({"error": "Estudiante no encontrado"}), 404

    est.activo = False
    db.session.commit()
    return jsonify({"mensaje": "Estudiante eliminado (borrado lógico)"}), 200

@estudiantes_bp.route("/<int:id>/kardex", methods=["GET"])
def obtener_kardex(id):
    est = Estudiante.query.get(id)
    if not est:
        return jsonify({"error": "Estudiante no encontrado"}), 404

    calificaciones = est.calificaciones
    if not calificaciones:
        return jsonify({
            "estudiante": est.to_dict(),
            "calificaciones": [],
            "mensaje": "El estudiante no tiene calificaciones registradas"
        }), 200

    valores = [c.calificacion for c in calificaciones]
    promedio = sum(valores) / len(valores)
    aprobadas = sum(1 for c in calificaciones if c.aprobado)
    reprobadas = len(calificaciones) - aprobadas

    return jsonify({
        "estudiante": est.to_dict(),
        "calificaciones": [c.to_dict() for c in calificaciones],
        "estadisticas": {
            "promedio_general": round(promedio, 2),
            "total_materias": len(calificaciones),
            "materias_aprobadas": aprobadas,
            "materias_reprobadas": reprobadas,
            "calificacion_maxima": max(valores),
            "calificacion_minima": min(valores),
            "estatus": "En riesgo" if promedio < 70 else "Regular" if promedio < 85 else "Excelente"
        }
    }), 200
