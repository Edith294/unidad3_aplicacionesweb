from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_class=None):
    app = Flask(__name__)

    if config_class is None:
        from app.config import Config
        app.config.from_object(Config)
    else:
        app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from app.routes.estudiantes import estudiantes_bp
        from app.routes.auth import auth_bp
        from app.routes.calificaciones import calificaciones_bp
        from app.routes.materias import materias_bp
        from app.routes.ordenes import ordenes_bp
        from app.routes.reportes import reportes_bp
        from app.routes.productos import productos_bp
        from app.routes.admin import admin_bp

        app.register_blueprint(estudiantes_bp, url_prefix="/api/estudiantes")
        app.register_blueprint(auth_bp, url_prefix="/api/auth")
        app.register_blueprint(calificaciones_bp, url_prefix="/api/calificaciones")
        app.register_blueprint(materias_bp, url_prefix="/api/materias")
        app.register_blueprint(ordenes_bp, url_prefix="/api/ordenes")
        app.register_blueprint(reportes_bp, url_prefix="/api/reportes")
        app.register_blueprint(productos_bp, url_prefix="/api/productos")
        app.register_blueprint(admin_bp, url_prefix="/api/admin")

    return app
