from sqlalchemy import create_engine, Column, Integer, Float, String, Date, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///shared_system.test.db')
Base = declarative_base()
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
    id_producto = Column(Integer, ForeignKey('productos.id_producto'), nullable=False)
    producto = relationship(Producto)
    cantidad = Column(Integer, nullable=False)
    precio_venta = Column(Float, nullable=False) 

class Despacho(Base):
    __tablename__ = 'despachos'

    id_despacho = Column(Integer, primary_key=True)
    fecha_despacho = Column(Date, nullable=False, default=datetime.utcnow)
    id_venta = Column(Integer, ForeignKey('ventas.id_venta'), nullable=False)
    direccion_envio = Column(String(255), nullable=False)
    estado = Column(String(255), nullable=False, default='Pendiente')
    venta = relationship(Venta)

Base.metadata.create_all(engine)
