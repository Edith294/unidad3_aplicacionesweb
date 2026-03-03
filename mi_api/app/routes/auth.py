from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app import db
from app.models.usuario import Usuario
from functools import wraps

auth_bp = Blueprint("auth", __name__)

def rol_requerido(*roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims.get("rol") not in roles:
                return jsonify({"error": "Acceso denegado. Permisos insuficientes"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

@auth_bp.route("/registro", methods=["POST"])
def registro():
    datos = request.get_json() or {}
    campos = ["username", "email", "password"]
    for c in campos:
        if c not in datos:
            return jsonify({"error": f"Falta el campo '{c}'"}), 400

    if Usuario.query.filter_by(username=datos["username"]).first():
        return jsonify({"error": "El username ya existe"}), 409

    if Usuario.query.filter_by(email=datos["email"]).first():
        return jsonify({"error": "El email ya está registrado"}), 409

    usuario = Usuario(
        username=datos["username"],
        email=datos["email"],
        rol=datos.get("rol", "docente")
    )
    usuario.set_password(datos["password"])
    db.session.add(usuario)
    db.session.commit()

    return jsonify({"id": usuario.id, "mensaje": "Usuario registrado exitosamente"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    datos = request.get_json() or {}
    usuario = Usuario.query.filter_by(username=datos.get("username")).first()

    if not usuario or not usuario.check_password(datos.get("password", "")):
        return jsonify({"error": "Credenciales incorrectas"}), 401

    token = create_access_token(
        identity=str(usuario.id),
        additional_claims={"rol": usuario.rol, "username": usuario.username}
    )

    return jsonify({
        "token": token,
        "tipo": "Bearer",
        "usuario": usuario.to_dict()
    }), 200

@auth_bp.route("/perfil", methods=["GET"])
@jwt_required()
def perfil():
    user_id = get_jwt_identity()
    usuario = Usuario.query.get(int(user_id))
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify({"usuario": usuario.to_dict()}), 200
