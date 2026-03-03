from app import db
from datetime import datetime

orden_producto = db.Table("orden_producto",
    db.Column("orden_id", db.Integer, db.ForeignKey("ordenes.id")),
    db.Column("producto_id", db.Integer, db.ForeignKey("productos.id")),
    db.Column("cantidad", db.Integer, default=1),
    db.Column("precio_unitario", db.Float)
)

class Orden(db.Model):
    __tablename__ = "ordenes"

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, default=0.0)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(30), default="completada")

    def to_dict(self):
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "total": self.total,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "estado": self.estado
        }
