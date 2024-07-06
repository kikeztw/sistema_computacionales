from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker
from flask import Flask, jsonify


engine = create_engine('sqlite:///shared_system.test.db')
Base = declarative_base()
app = Flask(__name__)
# Conexión a la base de datos SQLite

class Cliente(Base):
    __tablename__ = 'clientes'

    id_cliente = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)
    telefono = Column(String(255))
    direccion = Column(String(255))

class Producto(Base):
    __tablename__ = 'productos'

    id_producto = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text)

class Venta(Base):
    __tablename__ = 'ventas'

    id_venta = Column(Integer, primary_key=True)
    fecha_venta = Column(Date, nullable=False)
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'), nullable=False)
    cliente = relationship(Cliente)

    detalle_venta = relationship('VentaDetalle')

class VentaDetalle(Base):
    __tablename__ = 'venta_detalle'

    id_venta_detalle = Column(Integer, primary_key=True)
    id_venta = Column(Integer, ForeignKey('ventas.id_venta'), nullable=False)
    venta = relationship(Venta)
    id_producto = Column(Integer, ForeignKey('productos.id_producto'), nullable=False)
    producto = relationship(Producto)
    cantidad = Column(Integer, nullable=False)

Base.metadata.create_all(engine)
Session = sessionmaker(engine)

# Ruta principal (localhost:5000/)
@app.route('/')
def index():
    # Consulta para obtener los productos más vendidos
     # Crea una nueva sesión de SQLAlchemy
    productos_json = []
    with Session() as session:
      productos = session.query(Producto).all()
      for producto in productos:
              productos_json.append({
                  "id_producto": producto.id_producto,
                  "nombre": producto.nombre,
                  "descripcion": producto.descripcion,
              })
    
    return jsonify(productos_json)


if __name__ == '__main__':
    app.run(debug=True)