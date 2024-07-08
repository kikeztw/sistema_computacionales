from sqlalchemy import create_engine, Column, Integer, Float, String, Date, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from flask import Flask, jsonify, request, abort
from datetime import datetime

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
    precio_venta = Column(Float, nullable=False) 

Base.metadata.create_all(engine)
Session = sessionmaker(engine)

# Ruta principal (localhost:5000/)
@app.route('/')
def index():
    # Consulta para obtener los productos más vendidos
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

@app.route('/ventas', methods=['POST'])
def crear_ventas():
    """
    Crea un nuevo cliente, una venta y un detalle de venta en una sola transacción.
    Recibe un JSON con los datos del cliente y la venta.
    """
    datos_venta = request.get_json()

    if datos_venta is None:
        return abort(400, description="No se recibió información de la venta")

    nombre_cliente = datos_venta.get("nombre_cliente")
    id_producto = datos_venta.get("id_producto")
    cantidad = datos_venta.get("cantidad")
    precio_venta = datos_venta.get("precio_venta")
    fecha_venta = datos_venta.get("fecha_venta")

    if not nombre_cliente or not id_producto or not cantidad or not precio_venta or not fecha_venta:
        return abort(400, description="Faltan datos obligatorios para la venta")

    # Validación de datos (opcional, puedes agregarla aquí)
    # ... (código para validar la existencia de cliente, producto, stock, etc.)

    with Session() as session:
        try:
            # Crear el cliente si no existe (opcional)
            cliente_existente = session.query(Cliente).filter(Cliente.nombre == nombre_cliente).first()
            if not cliente_existente:
                nuevo_cliente = Cliente(nombre=nombre_cliente, telefono=datos_venta.get("telefono"), direccion=datos_venta.get("direccion"))
                session.add(nuevo_cliente)
                session.commit()
                id_cliente = nuevo_cliente.id_cliente
            else:
                id_cliente = cliente_existente.id_cliente

            # Crear la venta
            nueva_venta = Venta(
                id_cliente=id_cliente,
                fecha_venta=datetime.strptime(fecha_venta, '%Y-%m-%d')
            )
            session.add(nueva_venta)
            session.commit()  # Necesario para obtener el id_venta

            # Crear el detalle de venta
            nuevo_detalle = VentaDetalle(
                id_venta=nueva_venta.id_venta,
                id_producto=id_producto,
                cantidad=cantidad,
                precio_venta=precio_venta
            )
            session.add(nuevo_detalle)

            # Confirmar la transacción
            session.commit()

            # Retornar respuesta de éxito
            respuesta = {
                "mensaje": "Venta creada exitosamente",
                "datos": {
                    "id_venta": nueva_venta.id_venta,
                    "id_cliente": id_cliente,
                    "id_producto": id_producto,
                    "cantidad": cantidad,
                    "fecha_venta": nueva_venta.fecha_venta.strftime("%Y-%m-%d")
                }
            }
            return jsonify(respuesta), 201  # Código de estado 201 (Created)

        except Exception as e:
            # Revertir la transacción en caso de error
            session.rollback()
            raise e  # Propagar la excepción para un manejo adecuado del error

if __name__ == '__main__':
    app.run(debug=True)
