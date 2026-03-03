"""
Suite 5: Prueba End-to-End del flujo completo de la TechStore API.
"""
import pytest


class TestFlujoCOmpleto:

    @pytest.fixture(autouse=True)
    def setup_tienda(self, client):
        self.client = client
        self.token_admin = None
        self.token_cliente = None
        self.productos_creados = {}

    def _registrar_admin_y_productos(self, sufijo=""):
        self.client.post("/api/auth/registro", json={
            "username": f"admin_tienda{sufijo}", "email": f"admin{sufijo}@techstore.mx",
            "password": "Admin123!", "rol": "admin"
        })
        resp_login = self.client.post("/api/auth/login", json={
            "username": f"admin_tienda{sufijo}", "password": "Admin123!"
        })
        self.token_admin = resp_login.get_json()["token"]
        headers_admin = {"Authorization": f"Bearer {self.token_admin}"}

        productos = [
            {"sku": f"LAP001{sufijo}", "nombre": "Laptop Gamer 15", "precio": 18999.00, "stock": 10, "categoria_id": 1},
            {"sku": f"MOU001{sufijo}", "nombre": "Mouse Inalámbrico", "precio": 349.00, "stock": 50, "categoria_id": 2},
            {"sku": f"USB001{sufijo}", "nombre": "USB Hub 7 puertos", "precio": 199.00, "stock": 30, "categoria_id": 2},
        ]
        for prod in productos:
            resp = self.client.post("/api/productos/", json=prod, headers=headers_admin)
            assert resp.status_code == 201
            self.productos_creados[prod["sku"]] = resp.get_json()["producto"]

    def _registrar_cliente_y_login(self, sufijo=""):
        self.client.post("/api/auth/registro", json={
            "username": f"cliente01{sufijo}", "email": f"cliente{sufijo}@gmail.com",
            "password": "Cliente123!", "rol": "cliente"
        })
        resp = self.client.post("/api/auth/login", json={
            "username": f"cliente01{sufijo}", "password": "Cliente123!"
        })
        self.token_cliente = resp.get_json()["token"]

    def test_flujo_completo_compra(self):
        self._registrar_admin_y_productos(sufijo="A")
        assert len(self.productos_creados) == 3

        self._registrar_cliente_y_login(sufijo="A")
        assert self.token_cliente is not None

        headers_cliente = {"Authorization": f"Bearer {self.token_cliente}"}
        resp_busqueda = self.client.get("/api/productos/?buscar=laptop")
        assert resp_busqueda.status_code == 200
        resultados = resp_busqueda.get_json()["productos"]
        assert any("Laptop" in p["nombre"] for p in resultados)

        id_laptop = self.productos_creados["LAP001A"]["id"]
        id_mouse = self.productos_creados["MOU001A"]["id"]
        stock_inicial_laptop = self.productos_creados["LAP001A"]["stock"]

        resp_orden = self.client.post("/api/ordenes/", json={
            "cliente_id": 1,
            "productos": [
                {"producto_id": id_laptop, "cantidad": 2},
                {"producto_id": id_mouse, "cantidad": 5}
            ]
        }, headers=headers_cliente)
        assert resp_orden.status_code == 201
        orden = resp_orden.get_json()
        assert orden["productos_comprados"] == 2
        assert orden["total"] > 0
        assert "orden_id" in orden

        resp_prod = self.client.get(f"/api/productos/{id_laptop}")
        stock_actual = resp_prod.get_json()["stock"]
        assert stock_actual == stock_inicial_laptop - 2, \
            f"Stock debería ser {stock_inicial_laptop - 2}, es {stock_actual}"

        headers_admin = {"Authorization": f"Bearer {self.token_admin}"}
        resp_reporte = self.client.get("/api/reportes/ventas", headers=headers_admin)
        assert resp_reporte.status_code == 200
        reporte = resp_reporte.get_json()
        assert reporte["resumen"]["total_ordenes"] >= 1
        assert reporte["resumen"]["ingresos"] > 0
        assert len(reporte["top_productos"]) >= 1

    def test_orden_con_stock_insuficiente_falla(self):
        self._registrar_admin_y_productos(sufijo="B")
        self._registrar_cliente_y_login(sufijo="B")

        id_usb = self.productos_creados["USB001B"]["id"]
        headers_cliente = {"Authorization": f"Bearer {self.token_cliente}"}

        resp = self.client.post("/api/ordenes/", json={
            "cliente_id": 1,
            "productos": [{"producto_id": id_usb, "cantidad": 999}]
        }, headers=headers_cliente)
        assert resp.status_code == 400
        error = resp.get_json()
        assert "error" in error
        assert "stock" in str(error).lower()

        stock_usb = self.client.get(f"/api/productos/{id_usb}").get_json()["stock"]
        assert stock_usb == 30, "El stock no debe cambiar si la orden falla"

    def test_cliente_no_puede_ver_reporte_admin(self):
        self._registrar_cliente_y_login(sufijo="C")
        headers_cliente = {"Authorization": f"Bearer {self.token_cliente}"}
        resp = self.client.get("/api/reportes/ventas", headers=headers_cliente)
        assert resp.status_code == 403
