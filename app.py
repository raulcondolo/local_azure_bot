import os
from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

# Configuración de la conexión a la base de datos SQL usando variables de entorno
server = os.getenv('DB_SERVER')
database = os.getenv('DB_NAME')
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
driver= '{ODBC Driver 17 for SQL Server}'

def get_db_connection():
    conn = pyodbc.connect('DRIVER=' + driver +
                          ';SERVER=' + server +
                          ';PORT=1433' +
                          ';DATABASE=' + database +
                          ';UID=' + username +
                          ';PWD=' + password)
    return conn

@app.route('/bot', methods=['GET'])
def bot():
    pregunta = request.args.get('pregunta')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Respuesta FROM dbo.data_bot WHERE Pregunta = ?", pregunta)
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return jsonify({"respuesta": row[0]})
    else:
        return jsonify({"respuesta": "No tengo una respuesta para esa pregunta."})

if __name__ == '__main__':
    app.run(debug=True)
