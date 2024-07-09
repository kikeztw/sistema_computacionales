# Asignación 1

## Hurtado C., Castro J.
Pequeño ejemplo de dos aplicaciones que comparten una base de datos

## Requisitos
```sh
$ pip install flask, sqlalchemy
```
## Archivos 
- Aplicación de ventas: ventas.py
- Aplicación de despacho: despacho.py
- Solicitud de venta: data.json
- Soliditud de despacho: data1.json

## Ejecución
- Activar servidor de ventas
```sh
$ python venta.py 
```
- Activar servidor de despachos
```sh
$ python despacho.py 
```
- Realizar una venta
```sh
$ curl -X POST -H "Content-Type: application/json" -d @data.json http://localhost:5001/ventas
```
- Realizar un despacho
```sh
$ curl -X POST -H "Content-Type: application/json" -d @data1.json http://localhost:5000/despachos
```