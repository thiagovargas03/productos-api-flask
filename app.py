from flasgger import Swagger
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from os import environ 

load_dotenv()

app = Flask(__name__)   
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)
swagger = Swagger(app)

class Producto(db.Model):
    __tablename__ = 'Producto'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), nullable=False)
    descripcion = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)

    def json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': float(self.precio),
            'cantidad': self.cantidad
        }

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Servicio RESTful para Productos</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
                background-color: #f9f9f9;
            }
            h1 {
                color: #333;
            }
            p {
                font-size: 18px;
                color: #555;
            }
            a.button {
                display: inline-block;
                margin-top: 20px;
                padding: 10px 20px;
                background-color: #007BFF;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                font-size: 16px;
            }
            a.button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <h1>Servicio RESTful para gestion de productos</h1>
        <a href="/apidocs" class="button">Probar con Flasgger</a>
    </body>
    </html>
    """
    return html


@app.route('/producto', methods=['POST'])
def create_product():
    """
    Crear un nuevo producto
    ---
    tags:
      - Productos
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - nombre
            - descripcion
            - precio
            - cantidad
          properties:
            nombre:
              type: string
              example: "Remera"
            descripcion:
              type: string
              example: "Remera de algodon"
            precio:
              type: number
              format: float
              example: 1999.99
            cantidad:
              type: integer
              example: 10
    responses:
      201:
        description: Producto creado exitosamente
      500:
        description: Error en el servidor
    """
    try:
        data = request.get_json()
        print(data)
        new_product = Producto(
            nombre=data['nombre'],
            descripcion=data['descripcion'],
            precio=data['precio'],
            cantidad=data['cantidad']
        )
        db.session.add(new_product)
        db.session.commit()
        return make_response(jsonify({'message': 'Producto creado'}), 201)
    except Exception as e:
        print(e)  # para debug
        return make_response(jsonify({'message': 'Error creando producto'}), 500)


@app.route('/producto', methods=['GET'])
def get_products():
    """
    Obtener todos los productos
    ---
    tags:
      - Productos
    responses:
      200:
        description: Lista de productos
        content:
          application/json:
            schema:
              type: object
              properties:
                productos:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      nombre:
                        type: string
                      descripcion:
                        type: string
                      precio:
                        type: number
                        format: float
                      cantidad:
                        type: integer
      500:
        description: Error en el servidor
    """
    try:
        productos = Producto.query.all()
        return make_response(jsonify({'productos': [p.json() for p in productos]}), 200)
    except:
        return make_response(jsonify({'message': 'Error buscando productos'}), 500)

@app.route('/producto/<int:id>', methods=['GET'])
def get_product(id):
    """
    Obtener un producto por ID
    ---
    tags:
      - Productos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Producto encontrado
      404:
        description: Producto no encontrado
      500:
        description: Error en el servidor
    """
    try:
        product = Producto.query.filter_by(id=id).first()
        if product:
            return make_response(jsonify({'producto': product.json()}), 200)
        return make_response(jsonify({'message': 'Producto no encontrado'}), 404)
    except:
        return make_response(jsonify({'message': 'Error buscando el producto'}), 500)

@app.route('/producto/<int:id>', methods=['PUT'])
def update_product(id):
    """
    Actualizar un producto existente
    ---
    tags:
      - Productos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
              example: "Nombre actualizado"
            descripcion:
              type: string
              example: "Descripcion actualizada"
            precio:
              type: number
              format: float
              example: 2499.99
            cantidad:
              type: integer
              example: 5
    responses:
      200:
        description: Producto actualizado exitosamente
      404:
        description: Producto no encontrado
      500:
        description: Error en el servidor
    """
    try:
        product = Producto.query.get(id)
        if not product:
            return make_response(jsonify({'message': 'Producto no encontrado'}), 404)

        data = request.get_json()
        if 'nombre' in data:
            product.nombre = data['nombre']
        if 'descripcion' in data:
            product.descripcion = data['descripcion']
        if 'precio' in data:
            product.precio = data['precio']
        if 'cantidad' in data:
            product.cantidad = data['cantidad']

        db.session.commit()
        return make_response(jsonify({'message': 'Producto actualizado'}), 200)
    except:
        return make_response(jsonify({'message': 'Error actualizando producto'}), 500)


@app.route('/producto/<int:id>', methods=['DELETE'])
def delete_product(id):
    """
    Eliminar un producto por ID
    ---
    tags:
      - Productos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Producto eliminado
      404:
        description: Producto no encontrado
      500:
        description: Error en el servidor
    """
    try:
        product = Producto.query.filter_by(id=id).first()
        if product:
            db.session.delete(product)
            db.session.commit()
            return make_response(jsonify({'message': 'Producto eliminado'}), 200)
        return make_response(jsonify({'message': 'Producto no encontrado'}), 404)
    except:
        return make_response(jsonify({'message': 'Error eliminando producto'}), 500)

if __name__ == '__main__':
    app.run(debug=True)
