# 🛒 Productos
Servicio RESTful implementado en **Python + Flask**  con almacenamiento mediante **PostgreSQL**, y desplegado en **Render**.
Permite realizar operaciones CRUD sobre la entidad **PRODUCTOS**

---

## 🚀 Tecnologías

- Python 3.13
- Flask
- SQLAlchemy
- Psycopg2
- PostgreSQL
- Render

---

## 📖 Endpoints

Todos los ENDPOINTS señalados se encuentran documentados y ejemplificados con mayor detalle [en la colección de POSTMAN](https://github.com/thiagovargas03/productos-api-flask/blob/main/CRUD%20Producto%20API.postman_collection.json).

### 🔷 `POST /producto`
Permite crear un producto y almacenarlo en la base de datos.

### 🔷 `GET /producto`
Muestra todos los productos presentes en la base de datos.

### 🔷 `GET /producto/<id>`
Muestra solo el producto solicitado, con el id enviado por URL, desde la base de datos.

### 🔷 `PUT /producto/<id>`
Actualiza el producto solicitado, con el id enviado por URL, en la base de datos.

### 🔷 `DELETE /producto/<id>`
Elimina el producto solicitado, con el id enviado por la URL, de la base de datos.

---

## 🧰 Probar el servicio

El servicio se encuentra desplegado mediante Render, se pueden probar todos los ENDPOINTS [haciendo click aca](https://productos-api-flask.onrender.com/)


