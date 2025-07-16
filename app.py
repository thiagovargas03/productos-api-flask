from flasgger import Swagger
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ 

app = Flask(__name__)   
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)
swagger = Swagger(app)

class Producto(db.Model):
    __tablename__ = 'Producto'

    id = db.Column(db.Integer, primary_key=True)
    nombre= db.Column(db.String(30),nullable=False)
    descripcion= db.Column(db.String(100), nullable=False)
    precio= db.Column(db.Numeric(10,2), nullable=False)
    cantidad = db.Column(db.Integer,nullable=False)

    def json(self):
        return {'id':id,'nombre':self.nombre,'descripcion':self.descripcion,'precio':self.precio,'cantidad':self.cantidad}
db.create_all()

@app.route('/producto', methods = ['POST'])
def create_product():
    """
    Crear un nuevo producto
    ---
    tags:
      - Productos
    requestBody:
      required: true
      content:
        application/json:
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
              descripcion:
                type: string
              precio:
                type: number
                format: float
              cantidad:
                type: integer
    responses:
      201:
        description: Producto creado exitosamente
      500:
        description: Error en el servidor
    """
    try:
        data = request.get_json()
        new_product = Producto(nombre=data['nombre'],
                               descripcion=data['descripcion'],
                               precio=data['precio'],
                               cantidad=data['cantidad'])
        db.session.add(new_product)
        db.session.commit()
        return make_response(jsonify({'message':'Producto Creado'}),201)
    except:
        return make_response(jsonify({'message':'Error creando producto'}),500)
    

    
@app.route('/producto', methods = ['GET'])
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
        return make_response(jsonify({'Productos': [producto.json() for producto in productos]}), 200)
    except:
        return make_response(jsonify({'message':'Error buscando productos'}),500)
    
@app.route('/producto/<int:id>',methods=['GET'])
def get_product(id):
    try:
        product = Producto.query.filter_by(id=id).first()
        return make_response(jsonify({'Producto': product.json()}),200)
    except:
        return make_response(jsonify({{'message':'Error buscando el producto'}}))
    

    
@app.route('/producto/<int:id>', methods = ['PUT'])
def update_product(id):
    """
    Actualizar un producto por ID
    ---
    tags:
      - Productos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    requestBody:
      required: true
      content:
        application/json:
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
              descripcion:
                type: string
              precio:
                type: number
                format: float
              cantidad:
                type: integer
    responses:
      200:
        description: Producto actualizado
      404:
        description: Producto no encontrado
      500:
        description: Error en el servidor
    """
    try:
        product = Producto.query.filter_by(id = id).first()
        if product:
            data = request.get_json()
            product.nombre=data['nombre']
            product.descripcion=data['descripcion']
            product.precio=data['precio']
            product.cantidad=data['cantidad']
            db.session.commit()
            return make_response(jsonify({'message':'Producto Actualizado'}),201)
        return make_response(jsonify({'message':'Producto no encontrado'}),404)
    except:
        return make_response(jsonify({'message':'Error actualizando producto'}),500)
    
    
    
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
        product = Producto.query.filter_by(id = id).first()
        if product:
            db.session.delete(product)
            db.session.commit()
            return make_response(jsonify({'message':'Producto eliminado'}),200)
        return make_response(jsonify({'message':'Producto no encontrado'}),404)
    except:
        return make_response(jsonify({'message': 'Error eliminando producto'}),500)