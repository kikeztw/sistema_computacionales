from sqlalchemy import create_engine, Column, Integer, Float, String, Date, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from flask import Flask, jsonify, request, abort
from datetime import datetime
from bd import Despacho

engine = create_engine("sqlite:///shared_system.test.db")
Session = sessionmaker(bind=engine)
session = Session()


# Configuración de la aplicación Flask
app = Flask(__name__)

# Endpoint para crear un despacho
@app.route('/despachos', methods=['POST'])
def crear_despacho():
    session = Session()
    try:
        data = request.json

        nuevo_despacho = Despacho(
            id_venta=data['id_venta'],
            direccion_envio=data['direccion_envio'],
            estado=data.get('estado', 'Pendiente')  # Estado es opcional, por defecto 'Pendiente'
        )

        session.add(nuevo_despacho)
        session.commit()

        return jsonify({'message': 'Despacho creado exitosamente'}), 201

    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        session.close()

if __name__ == '__main__':
    app.run(debug=True)
