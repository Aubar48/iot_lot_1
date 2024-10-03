from flask import Flask, request, jsonify, Response, render_template
import mysql.connector
from mysql.connector import Error
from functools import wraps

app = Flask(__name__)

# Función para establecer conexión con la base de datos
def connect_db():
    try:
        return mysql.connector.connect(
            host="bxy5ofa8ezud0x0caavs-mysql.services.clever-cloud.com",
            user="uupemiqze1zhijfn",
            password="XnExGlv7QzWuydrfjtLK",  # Cambia las credenciales según tu configuración
            database="bxy5ofa8ezud0x0caavs"
        )
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Autenticación básica
def authenticate(username, password):
    return username == 'uupemiqze1zhijfn' and password == 'XnExGlv7QzWuydrfjtLK'  # Cambia las credenciales según tus necesidades

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not authenticate(auth.username, auth.password):
            return Response('Acceso no permitido', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return f(*args, **kwargs)
    return decorated

# Endpoint para la página principal
@app.route('/')
def index():
    return render_template('index.html')  # Asegúrate de que index.html esté en la carpeta templates

# Endpoint para recibir y almacenar datos
@app.route('/data', methods=['POST'])
@require_auth  # Protege esta ruta con autenticación
def receive_data():
    data = request.json
    print("Datos recibidos:", data)

    if not all(k in data for k in ('sensor', 'value')):
        print("Error: Faltan campos 'sensor' o 'value'")
        return jsonify({"error": "Faltan datos 'sensor' o 'value'"}), 400

    sensor = data['sensor']
    value = data['value']
    print(f"Sensor: {sensor}, Value: {value}")

    db = connect_db()
    if db is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    try:
        cursor = db.cursor()
        sql = "INSERT INTO sensor_data (sensor, value) VALUES (%s, %s)"
        cursor.execute(sql, (sensor, value))
        db.commit()
        print("Datos insertados en la base de datos correctamente")
    except Error as e:
        print(f"Error al insertar datos en la base de datos: {e}")
        return jsonify({"error": f"Error al insertar datos: {e}"}), 500
    finally:
        cursor.close()
        db.close()

    return jsonify({"message": "Datos recibidos y almacenados correctamente"}), 200

# Endpoint para recuperar datos
@app.route('/data', methods=['GET'])
@require_auth  # Protege esta ruta con autenticación
def get_data():
    db = connect_db()
    if db is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    cursor = db.cursor()
    cursor.execute("SELECT * FROM sensor_data")
    results = cursor.fetchall()
    cursor.close()
    db.close()

    data = [{"id": row[0], "sensor": row[1], "value": row[2], "timestamp": row[3]} for row in results]
    return jsonify(data), 200

# Endpoint para actualizar datos
@app.route('/data/<int:id>', methods=['PUT'])
@require_auth  # Protege esta ruta con autenticación
def update_data(id):
    data = request.json
    if 'sensor' not in data or 'value' not in data:
        return jsonify({"error": "Faltan datos 'sensor' o 'value'"}), 400

    sensor = data['sensor']
    value = data['value']

    db = connect_db()
    if db is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    try:
        cursor = db.cursor()
        sql = "UPDATE sensor_data SET sensor = %s, value = %s WHERE id = %s"
        cursor.execute(sql, (sensor, value, id))
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Registro no encontrado"}), 404

    except Error as e:
        return jsonify({"error": f"Error al actualizar datos: {e}"}), 500
    finally:
        cursor.close()
        db.close()

    return jsonify({"message": "Datos actualizados correctamente"}), 200

# Endpoint para eliminar datos
@app.route('/data/<int:id>', methods=['DELETE'])
@require_auth  # Protege esta ruta con autenticación
def delete_data(id):
    db = connect_db()
    if db is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    try:
        cursor = db.cursor()
        sql = "DELETE FROM sensor_data WHERE id = %s"
        cursor.execute(sql, (id,))
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Registro no encontrado"}), 404

    except Error as e:
        return jsonify({"error": f"Error al eliminar datos: {e}"}), 500
    finally:
        cursor.close()
        db.close()

    return jsonify({"message": "Registro eliminado correctamente"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
