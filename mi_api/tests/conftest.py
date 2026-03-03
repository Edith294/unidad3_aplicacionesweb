import pytest
from app import create_app, db as _db
from app.config import TestingConfig

# ─── Fixture: Aplicación de prueba ───────────────────────────────────
@pytest.fixture(scope="session")
def app():
    app = create_app(TestingConfig)
    yield app

# ─── Fixture: Base de datos (scope session) ──────────────────────────
@pytest.fixture(scope="session")
def db(app):
    with app.app_context():
        _db.create_all()
        yield _db
        _db.drop_all()

# ─── Fixture: Limpieza de tablas entre pruebas ───────────────────────
@pytest.fixture(scope="function", autouse=True)
def limpiar_tablas(db, app):
    """Borra todos los datos entre pruebas para que sean independientes."""
    yield
    with app.app_context():
        # Limpiar en orden correcto por las foreign keys
        from app.models.calificacion import Calificacion
        from app.models.orden import Orden
        from app.models.estudiante import Estudiante
        from app.models.usuario import Usuario
        from app.models.materia import Materia
        from app.models.producto import Producto
        _db.session.query(Calificacion).delete()
        _db.session.query(Orden).delete()
        _db.session.query(Estudiante).delete()
        _db.session.query(Usuario).delete()
        _db.session.query(Materia).delete()
        _db.session.query(Producto).delete()
        _db.session.commit()

# ─── Fixture: session para pruebas de modelos ────────────────────────
@pytest.fixture(scope="function")
def session(db, app):
    with app.app_context():
        yield _db.session

# ─── Fixture: Cliente HTTP de prueba ─────────────────────────────────
@pytest.fixture(scope="function")
def client(app, db):
    """El parámetro db garantiza que las tablas ya existen antes de cada prueba."""
    with app.app_context():
        with app.test_client() as c:
            yield c

# ─── Fixture: Datos de estudiante de prueba ──────────────────────────
@pytest.fixture
def estudiante_data():
    return {
        "matricula": "TEST001",
        "nombre": "Carlos",
        "apellido": "Ramírez",
        "email": "carlos@test.edu.mx",
        "carrera": "ITIC",
        "semestre": 5
    }

# ─── Fixture: Token JWT de prueba ────────────────────────────────────
@pytest.fixture
def auth_headers(client):
    client.post("/api/auth/registro", json={
        "username": "docente_test", "email": "doc@test.mx",
        "password": "Password123!", "rol": "docente"
    })
    resp = client.post("/api/auth/login", json={
        "username": "docente_test", "password": "Password123!"
    })
    token = resp.get_json()["token"]
    return {"Authorization": f"Bearer {token}"}
