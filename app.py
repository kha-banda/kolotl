from flask import Flask, redirect, render_template, request, url_for, session, flash
import mysql.connector
import time  # Importar el módulo time
from datetime import datetime
import plotly.graph_objs as go
from functools import wraps
from flask import jsonify
from geopy.distance import geodesic
import math
from geopy.geocoders import Nominatim
import requests
from mysql.connector import pooling
import os
from flask import jsonify
import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

app = Flask(__name__)

# Tu clave de API de HERE
HERE_API_KEY = '1F91LCxBz_coxRzfxs5qybZKq0a-09Q40EyQMsP_ehA'
OPEN_WEATHER_MAP = '0c92193205b8016c9c0cedc51ebd650b'
app.secret_key = 'kolotl_unca'  # Necesario para gestionar sesiones
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
# Tu API Key de OpenWeatherMap
API_KEY = "ec66f746a0e14f57ac1152001242911"
# Conexión a la base de datos MySQL usando mysql-connector
# Configuración del pool de conexiones
pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=25,
    host='69.62.71.171',
    user='root',
    password='caravanadestrucs',
    database='scorpions'
)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from flask import request
# Crear la carpeta si no existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def build_breadcrumbs(path):
    parts = path.strip('/').split('/')
    breadcrumbs = []
    url = ''
    
    for i, part in enumerate(parts):
        url += '/' + part
        is_last = (i == len(parts) - 1)

        part_display = part.capitalize()
        
        breadcrumbs.append({
            'name': part_display,
            'url': None if is_last else url
        })

    return breadcrumbs



# Decorador para verificar si el usuario está autenticado
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session:
            flash('Por favor, inicie sesión para acceder a esta página.', 'warning')
            return redirect(url_for('login'))  # Redirige a la página de inicio de sesión si no está autenticado
        return f(*args, **kwargs)
    return decorated_function
# Ruta principal protegida por sesión  


@app.route('/')
def Index():
    path = request.path  # obtiene la ruta actual
    breadcrumbs = build_breadcrumbs(path)
    if 'loggedin' in session:
        return render_template('index.html',session = session,breadcrumbs=breadcrumbs )
    else:
        return render_template('index.html')


###################################################################     
#usuarios-admin                                                   #
###################################################################
@app.route('/Usuarios')
@login_required  # Esto asegura que solo usuarios autenticados puedan acceder a esta ruta
def users():
    path = request.path  # obtiene la ruta actual
    breadcrumbs = build_breadcrumbs(path)
    if 'loggedin' in session and session['rol'] == "admin":
        
        usuarios = get_all_users()
        return render_template('Users.html',session = session,usuarios = usuarios,breadcrumbs=breadcrumbs )
    else:
        return redirect(url_for('Index'))

# Ruta para crear un nuevo usuario
@app.route('/crear_usuario', methods=['POST'])
@login_required
def crear_usuario():
    try:
        # Obtén los datos de la solicitud
        data = request.json  # Asegúrate de enviar datos JSON en el cuerpo
        print(data)
        # Llama a la función create_user
        user_id = create_user(data)
        if user_id:
              return jsonify({"success": True, "message": "Usuario creado exitosamente", "user_id": user_id}), 201
        else:
            return jsonify({"success": False, "error": "No se pudo crear el usuario"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para obtener los detalles de un usuario por su ID
@app.route('/obtener_usuario/<int:id>', methods=['GET'])
@login_required
def obtener_usuario(id):
    
    connection = pool.get_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE ID = %s', [id])
    usuario = cursor.fetchone()
    cursor.close()
    connection.close()
    if usuario:
        return jsonify(usuario)
   
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404
# Ruta para actualizar un usuario existente
@app.route('/actualizar_usuario/<int:id>', methods=['POST'])
@login_required
def actualizar_usuario(id):
    connection = pool.get_connection()
    cursor = connection.cursor()
    nombre = request.form['editar-nombre']
    apellido = request.form['editar-apellido']
    correo = request.form['editar-correo']
    rol = request.form['editar-rol']
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        'UPDATE usuarios SET nombre = %s, apellido = %s, correo = %s, rol = %s, ultima_actualizacion = NOW() WHERE ID = %s',
        (nombre, apellido, correo, rol, id)
    )
    connection.commit()
    cursor.close()
    connection.close()
    if cursor.rowcount > 0:
        return jsonify({'success': True})
    return jsonify({'error': 'Usuario no encontrado'}), 404
# Ruta para eliminar un usuario
@app.route('/eliminar_usuario/<int:id>', methods=['POST'])
@login_required
def eliminar_usuario(id):
    connection = pool.get_connection()
    cursor = connection.cursor()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('DELETE FROM usuarios WHERE id = %s', [id])
    connection.commit()
    cursor.close()
    connection.close()
    if cursor.rowcount > 0:
        return jsonify({'success': True})
    return jsonify({'error': 'Usuario no encontrado'}), 404




@app.route('/capturas')
def capturas():
    if 'loggedin' in session:
        connection = pool.get_connection()
        cursor = connection.cursor()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM scorpions')
        scorpiones = cursor.fetchall()
        # Convertir los datos a un formato más amigable
        scorpion_data = []
        for row in scorpiones:
            scorpion_data.append({
                'ID': row['ID'],
                'orden': row['orden'],
                'familia': row['familia'],
                'genero': row['genero'],
                'especie': row['especie'],
            })
        cursor.execute('SELECT * FROM habitat')
        habitat = cursor.fetchall()
        # Convertir los datos a un formato más amigable
        habitats = []
        for row in habitat:
            habitats.append({
                'ID': row['ID'],
                'nombre': row['nombre'],
            })
        cursor.close()
        connection.close()
        path = request.path  # obtiene la ruta actual
        breadcrumbs = build_breadcrumbs(path)
        return render_template('capturas.html',session = session,scorpiones = scorpion_data,habitats = habitats ,breadcrumbs=breadcrumbs  )
    else:
        return render_template('index.html')

from flask import jsonify, request

@app.route('/delete_capture/<int:capture_id>', methods=['DELETE'])
@login_required
def delete_capture(capture_id):
    try:
        result, status_code = eliminar_recolecta(capture_id)
        return jsonify(result), status_code
    except Exception as e:
        # Log detallado para el servidor
        print(f"Error deleting capture: {e}")
        # Respuesta genérica al cliente
        return jsonify({'error': 'Failed to delete capture.'}), 500


@app.route('/registro_captura', methods=['POST'])
@login_required
def submit_data():
    # Recibir los datos del formulario enviados por el modal
    try:
      # Procesa la solicitud JSON
        import json
        connection = pool.get_connection()
        data = request.get_json()

        # Sección de Ubicación
        latitud = data.get('latitud', 'No especificada')
        longitud = data.get('longitud', 'No especificada')
        pais = data.get('pais', 'No especificado')
        estado = data.get('estado', 'No especificado')
        ciudad = data.get('ciudad', 'No especificada')
        colonia = data.get('colonia', 'No especificada')
        # Sección de Datos Taxonómicos
        orden = data.get('orden', 'No especificado')
        familia = data.get('familia', 'No especificada')
        genero = data.get('genero', 'No especificado')
        especie = data.get('especie', 'No especificada')
        # Sección de Conteo de Alacranes
        adultos_macho = int(data.get('adultos-macho', 0))
        adultos_hembra = int(data.get('adultos-hembra', 0))
        jovenes_macho = int(data.get('jovenes-macho', 0))
        jovenes_hembra = int(data.get('jovenes-hembra', 0))
        subadultos_macho = int(data.get('subadultos-macho', 0))
        subadultos_hembra = int(data.get('subadultos-hembra', 0))
        habitat = data.get('habitatSelect', 0)
        fecha_captura = data.get('fechaCaptura', 'No especificada')
        notas = data.get('notas', '')
                
        if fecha_captura:
            try:
                # Intentar convertir `fechaCaptura` en un objeto datetime
                fecha_obj = datetime.strptime(fecha_captura, "%Y-%m-%dT%H:%M")
            except ValueError:
                # Manejar un formato incorrecto
                raise ValueError("El formato de 'fechaCaptura' debe ser YYYY-MM-DDTHH:MM.")
        else:
            # Si no se proporciona fecha, usar la fecha y hora actual
            fecha_obj = datetime.now()

        # Formatear como lo necesites (por ejemplo, solo fecha o fecha y hora)
        fecha_formateada = fecha_obj.strftime('%Y-%m-%d')  # Solo la fecha
        hora_formateada = fecha_obj.strftime('%H:%M')      # Solo la hora
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM locacion WHERE  pais = %s and estado = %s and municipio = %s and colonia  = %s ', [ pais, estado, ciudad, colonia])
        locacion = cursor.fetchone()
        id_locacion = ""
        if locacion:
            id_locacion = locacion['ID']  # Almacena el ID de la locacion
        else:
            cursor.execute(
                'INSERT INTO locacion ( cp, pais, estado, municipio, colonia, fecha_creacion, ultima_actualizacion) VALUES (%s,%s,%s,%s,%s, NOW(), NOW())',
            (" ",pais,estado,ciudad,colonia)

            )
            connection.commit()
            
            # Obtener el ID del registro insertado
            id_locacion = cursor.lastrowid
        cursor.execute('SELECT * FROM scorpions WHERE  orden = %s and familia = %s and genero = %s and especie  = %s ', [orden, familia, genero, especie])
        scorpion = cursor.fetchone()
        id_scorpion = ""
        if scorpion:
            id_scorpion = scorpion['ID']
        else:
            return jsonify({'error':' escorpion no encontrado.'}), 500
        cursor = connection.cursor()
            
        # Consulta SQL de inserción
        query = """
                INSERT INTO `recolecta`(
                    `fecha_captura`, `adultomacho`, `adultohembra`, 
                    `juvenilmacho`, `juvenilhembra`, `subadultomacho`, `subadultohembra`, 
                    `notas`, `ID_usuario`, `ID_locacion`, `ID_habitat`, `ID_scorpion`, 
                    `fecha_creacion`, `ultima_actualizacion`
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,NOW(), NOW())
            """
            
        # Valores a insertar
        values = (
                fecha_formateada,adultos_macho,adultos_hembra,
                jovenes_macho,jovenes_hembra, subadultos_macho, subadultos_hembra,
                notas, session['id'],id_locacion,habitat,
                id_scorpion
            )
            
        # Ejecutar la consulta
        cursor.execute(query, values)
        connection.commit()
        # Obtener el ID del registro insertado
        id_captura = cursor.lastrowid
        temperatura= obtener_clima_fecha(latitud,longitud,fecha_formateada,API_KEY,OPEN_WEATHER_MAP,hora_formateada)
        cursor = connection.cursor()

        # Consulta SQL de inserción
        query = """
                INSERT INTO `coordenadas_recolecta`(
                    `lat`, `longitud`, `ALT`, `temperatura`, `humedad`, `ID_recolecta`
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """
            
        # Valores a insertar
        values = (
                latitud, longitud, temperatura['altitud'],
                temperatura['temperatura_min'], temperatura['humedad'], id_captura
            )
            
        # Ejecutar la consulta
        cursor.execute(query, values)
        connection.commit()
        print(f"Registro insertado exitosamente con ID_coordenadas: {cursor.lastrowid}")
        print("Registro insertado exitosamente.")

        cursor.close()
        connection.close()
        return jsonify({'success': 'Datos guardados correctamente.'}), 200
    except Exception as e:
        print(f"Error al procesar los datos: {e}")
        return jsonify({'error': 'Hubo un error al procesar los datos.'}), 500

@app.route('/actualizar_captura', methods=['POST'])
@login_required
def actualizar_captura():
    try:
        connection = pool.get_connection()
        # Obtener el ID de la captura que se desea actualizar
        captura_id = request.form.get('captura_id')
        
        # Verificar si el ID de captura es válido
        if not captura_id:
            return jsonify({'error': 'ID de captura no proporcionado.'}), 400

        # Sección de Ubicación
        latitud = request.form.get('latitud')
        longitud = request.form.get('longitud')
        pais = request.form.get('pais')
        estado = request.form.get('estado')
        ciudad = request.form.get('ciudad')
        colonia = request.form.get('colonia')
        
        # Sección de Datos Taxonómicos
        orden = request.form.get('orden')
        familia = request.form.get('familia')
        genero = request.form.get('genero')
        especie = request.form.get('especie')

        # Sección de Conteo de Alacranes
        adultos_macho = int(request.form.get('adultos-macho', 0))
        adultos_hembra = int(request.form.get('adultos-hembra', 0))
        jovenes_macho = int(request.form.get('jovenes-macho', 0))
        jovenes_hembra = int(request.form.get('jovenes-hembra', 0))
        subadultos_macho = int(request.form.get('subadultos-macho', 0))
        subadultos_hembra = int(request.form.get('subadultos-hembra', 0))
        habitat = int(request.form.get('habitatSelect', 0))
        fecha_captura = request.form.get('fecha_captura', '')
        notas = request.form.get('notas', '')

        cursor = connection.cursor(dictionary=True)

        # Buscar o insertar ubicación
        cursor.execute('SELECT * FROM locacion WHERE pais = %s and estado = %s and municipio = %s and colonia = %s', 
                       [pais, estado, ciudad, colonia])
        locacion = cursor.fetchone()
        id_locacion = ""
        if locacion:
            id_locacion = locacion['ID']
        else:
            cursor.execute(
                'INSERT INTO locacion (cp, pais, estado, municipio, colonia, fecha_creacion, ultima_actualizacion) VALUES (%s,%s,%s,%s,%s, NOW(), NOW())',
                (" ", pais, estado, ciudad, colonia)
            )
            connection.commit()
            id_locacion = cursor.lastrowid

        # Buscar escorpión
        cursor.execute('SELECT * FROM scorpions WHERE orden = %s and familia = %s and genero = %s and especie = %s', 
                       [orden, familia, genero, especie])
        scorpion = cursor.fetchone()
        id_scorpion = ""
        if scorpion:
            id_scorpion = scorpion['ID']
        else:
            return jsonify({'error': 'Escorpión no encontrado.'}), 500

        # Actualizar datos de la captura
        cursor.execute(
            """
            UPDATE recolecta 
            SET 
                fecha_captura = %s, adultomacho = %s, adultohembra = %s, juvenilmacho = %s, juvenilhembra = %s, 
                subadultomacho = %s, subadultohembra = %s, lat = %s, longitud = %s, ALT = 'Desconocido', notas = %s, 
                ID_usuario = %s, ID_locacion = %s, ID_habitat = %s, ID_scorpion = %s, ultima_actualizacion = NOW()
            WHERE 
                ID = %s
            """,
            (fecha_captura, adultos_macho, adultos_hembra, jovenes_macho, jovenes_hembra, subadultos_macho, subadultos_hembra, 
             latitud, longitud, notas, session['id'], id_locacion, habitat, id_scorpion, captura_id)
        )
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'success': 'Datos actualizados correctamente.'}), 200
    except Exception as e:
        print(f"Error al procesar los datos: {e}")
        return jsonify({'error': 'Hubo un error al procesar los datos.'}), 500



@app.route('/get_captures', methods=['GET'])
def get_captures():
    try:
        id_scorpion = request.args.get('id_scorpion')
        # Llama a la función y desestructura los datos y el código HTTP
        data, status_code = obtener_recolectas(id_scorpion) if id_scorpion else obtener_recolectas()
        return jsonify(data), status_code
    except Exception as e:
        print(f"Error retrieving captures: {e}")
        return jsonify({'error': 'Failed to retrieve capture data.'}), 500


@app.route('/get_captures_data', methods=['GET'])
def get_captures_data():
    try:
        id_scorpion = request.args.get('id_scorpion')  # Filtro opcional

        connection = pool.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Consulta base con filtro opcional
        query = "SELECT * FROM recolecta"
        params = ()

        if id_scorpion:
            query += " WHERE ID_scorpion = %s"
            params = (id_scorpion,)
        
        cursor.execute(query, params)
        capturas = cursor.fetchall()

        total_captures = len(capturas)
        total_scorpions = sum(row['adultomacho'] + row['adultohembra'] + row['juvenilmacho'] + row['juvenilhembra']
                              + row['subadultomacho'] + row['subadultohembra'] for row in capturas)
        
        habitats_count = {}
        species_count = {}
        captures = []

        for row in capturas:
            cursor.execute("""
                SELECT 
                    habitat.nombre AS habitat_name,
                    scorpions.familia AS species_family,
                    scorpions.genero AS species_genero,
                    scorpions.especie AS species_name,
                    locacion.estado AS estado,
                    locacion.municipio AS municipio,
                    usuarios.nombre AS usuario_nombre,
                    usuarios.apellido AS usuario_apellido
                FROM recolecta
                LEFT JOIN habitat ON recolecta.ID_habitat = habitat.ID
                LEFT JOIN scorpions ON recolecta.ID_scorpion = scorpions.ID
                LEFT JOIN locacion ON recolecta.ID_locacion = locacion.ID
                LEFT JOIN usuarios ON recolecta.ID_usuario = usuarios.ID
                WHERE recolecta.ID = %s
            """, (row['ID'],))
            result = cursor.fetchone()

            habitat_name = result['habitat_name'] if result['habitat_name'] else 'Unknown'
            species_name = result['species_name'] if result['species_name'] else 'Unknown'
            species_family = result['species_family'] if result['species_family'] else 'Unknown'
            species_genero = result['species_genero'] if result['species_genero'] else 'Unknown'
            locacion = {'estado': result['estado'], 'municipio': result['municipio']}
            persona = {'nombre': result['usuario_nombre'], 'apellido': result['usuario_apellido']}

            habitats_count[habitat_name] = habitats_count.get(habitat_name, 0) + 1
            species_count[species_name] = species_count.get(species_name, 0) + 1

            captures.append({
                'ID': row['ID'],
                'ID_usuario': row['ID_usuario'],
                'persona': persona,
                'fecha_captura': row['fecha_captura'],
                'adultomacho': row['adultomacho'],
                'adultohembra': row['adultohembra'],
                'juvenilmacho': row['juvenilmacho'],
                'juvenilhembra': row['juvenilhembra'],
                'subadultomacho': row['subadultomacho'],
                'subadultohembra': row['subadultohembra'],
                'locacion': locacion,
                'habitat': habitat_name,
                'escorpion': species_name,
                'species_family': species_family,
                'species_genero': species_genero
            })

        cursor.close()
        connection.close()

        return jsonify({
            'captures': captures,
            'statistics': {
                'total_captures': total_captures,
                'total_scorpions': total_scorpions,
                'habitats_count': habitats_count,
                'species_count': species_count
            }
        }), 200

    except Exception as e:
        print(f"Error retrieving capture data: {e}")
        return jsonify({'error': 'Failed to retrieve capture data.'}), 500

# Función para obtener la ubicación usando HERE.com
def obtener_ubicacion(latitud, longitud):
    # Definir la URL de la API de HERE
    url = "https://revgeocode.search.hereapi.com/v1/revgeocode"

    # Parámetros para la solicitud
    params = {
        'at': f'{latitud},{longitud}',
        'apikey': HERE_API_KEY
    }

    # Realizar la solicitud a la API de HERE
    respuesta = requests.get(url, params=params)

    if respuesta.status_code == 200:
        data = respuesta.json()

        if data and 'items' in data and len(data['items']) > 0:
            # Obtener la primera ubicación encontrada
            ubicacion = data['items'][0]['address']

            pais = ubicacion.get('countryName', 'Desconocido')
            estado = ubicacion.get('state', 'Desconocido')
            municipio = ubicacion.get('city', ubicacion.get('adminLevel2', 'Desconocido'))  # Verificar niveles alternativos
            colonia = ubicacion.get('district', ubicacion.get('subregion', 'Desconocido'))  # Otra opción si no detecta colonia
            codigo_postal = ubicacion.get('postalCode', 'Desconocido')

            return {
                'pais': pais,
                'estado': estado,
                'municipio': municipio,
                'colonia': colonia,
                'codigo_postal': codigo_postal
            }
        else:
            return None
    else:
        return None

# Ruta para manejar la solicitud GET y obtener la ubicación
@app.route('/ubicacion', methods=['GET'])
def obtener_ubicacion_api():
    latitud = request.args.get('latitud', type=float)
    longitud = request.args.get('longitud', type=float)

    if latitud is None or longitud is None:
        return jsonify({"error": "Debe proporcionar latitud y longitud"}), 400

    ubicacion = obtener_ubicacion(latitud, longitud)

    if ubicacion:
        return jsonify(ubicacion), 200
    else:
        return jsonify({"error": "No se encontró información para las coordenadas proporcionadas"}), 404




# Ruta de inicio de sesión (login)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        connection = pool.get_connection()
        # Obtén los datos del formulario
        email = request.form['email']
        password = request.form['password']
        
        # Verifica las credenciales en la base de datos
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios WHERE correo = %s AND contrasena = %s', (email, password))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        if user:
            # Si el usuario es válido, guarda los datos en la sesión
            session['loggedin'] = True
            session['id'] = user['ID']  # Almacena el ID del usuario
            session['email'] = user['correo']
            session['nombre'] = user['nombre']  # Almacena el email
            session['rol'] = user['rol']
            flash('Inicio de sesión exitoso!', 'success')
            print("exito")
            return redirect(url_for('Index'))
        else:
            print("error")
            flash('Correo o contraseña incorrectos!', 'danger')
    
    return redirect(url_for('Index'))

# Ruta de cierre de sesión (logout)
@app.route('/logout')
def logout():
    # Elimina los datos de sesión
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    session.pop('nombre', None)
    flash('Has cerrado sesión', 'success')
    return redirect(url_for('login'))

# Ruta para agregar contacto (ejemplo de inserción a la base de datos)
@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        connection = pool.get_connection()
        rol_var = request.form['ID']
        correo_var = request.form['Email']
        name_var = request.form['Nombre']
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (role_id, email, first_name) VALUES (%s, %s, %s)', (rol_var, correo_var, name_var))
        connection.commit()
        cursor.close()
        connection.close()
        flash('Contacto añadido exitosamente!', 'success')
        return redirect(url_for('Index'))

# Ruta para eliminar un contacto (ejemplo de eliminación de la base de datos)
@app.route('/delete_contact/<string:id>')
def delete_contact(id):
    connection = pool.get_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM users WHERE id = %s', (id,))
    connection.commit()
    connection.close()
    cursor.close()
    flash('Contacto eliminado exitosamente!', 'success')
    return redirect(url_for('Index'))

# Ruta para visualizar estadísticas (ejemplo de gráficos con Plotly)
@app.route('/Estadisticas')
def estadisticas():
    path = request.path  # obtiene la ruta actual
    breadcrumbs = build_breadcrumbs(path)
    x_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    y_data = [10, 15, 20, 12, 78, 30, 13, 34, 23, 56, 12, 89]
    trace = go.Scatter(x=x_data, y=y_data, mode='lines+markers', name='Datos Ejemplo')
    data = [trace]
    layout = go.Layout(title='No. Especies Encontradas 2023', xaxis=dict(title='Meses'), yaxis=dict(title='No. Especies'))
    fig = go.Figure(data=data, layout=layout)
    graph_json = fig.to_json()

    x1_data = [2020, 2021, 2022, 2023]
    y2_data = [100, 78, 45, 200]
    trace1 = go.Scatter(x=x1_data, y=y2_data, mode='lines+markers', name='Registro de alacranes')
    data1 = [trace1]
    layout1 = go.Layout(title='Especies por año encontradas', xaxis=dict(title='Años'), yaxis=dict(title='No. de Especies'))
    fig1 = go.Figure(data=data1, layout=layout1)
    graph2_json = fig1.to_json()

    data_barras = {
        'anos': ['2018', '2019', '2020', '2021'],
        'Publica': [10, 40, 30, 4]
    }

    return render_template('estadisticas.html', graphJSON=graph_json, graph2JSON=graph2_json, data_barras=data_barras,breadcrumbs=breadcrumbs )

# Rutas adicionales de la página
@app.route('/Galeria Escorpiones')
def galeria():
    path = request.path
    breadcrumbs = build_breadcrumbs(path)
    scorpion_data = get_all_scorpions()
    # Verifica si llegaron parámetros GET
    if request.args:  # Esto verifica si hay al menos un parámetro
        # Si no hay parámetros GET, muestra la galería base
        return render_template('index-2.html', breadcrumbs=breadcrumbs)
    else:
        # Si no hay parámetros GET, muestra la galería base
        return render_template('index-2.html',scorpion_data = scorpion_data , breadcrumbs=breadcrumbs)
@app.route('/Galeria Escorpiones/Escorpion/')
def galeria_escorpion():
    id_scorpion = request.args.get('id_scorpion')  # Filtro opcional
    path = request.path

    breadcrumbs = build_breadcrumbs(path)
    scorpion_data = get_scorpion_by_id(id_scorpion)
    breadcrumbs.append({
            'name': scorpion_data['genero']+" "+ scorpion_data['especie'],
            'url': None
        })
    return render_template('escorpion.html',scorpion_data=scorpion_data  , breadcrumbs=breadcrumbs)

@app.route('/Mapa')
def map():
    path = request.path  # obtiene la ruta actual
    breadcrumbs = build_breadcrumbs(path)
    return render_template('map.html',breadcrumbs = breadcrumbs)
@app.route('/Acerca')
def acerca():
    path = request.path  # obtiene la ruta actual
    breadcrumbs = build_breadcrumbs(path)
    return render_template('index-3.html',breadcrumbs = breadcrumbs)
@app.route('/Galeria_imagenes')
def galeria_imagenes():
    path = request.path  # obtiene la ruta actual
    breadcrumbs = build_breadcrumbs(path)
    return render_template('galeria.html',breadcrumbs = breadcrumbs)

@app.route('/scorpiones')
@login_required  # Esto asegura que solo usuarios autenticados puedan acceder a esta ruta
def scorpiones():
     path = request.path  # obtiene la ruta actual
     breadcrumbs = build_breadcrumbs(path)
     if 'loggedin' in session and session['rol'] == "admin":
        scorpion_data = get_all_scorpions()
        return render_template('scorpions.html',scorpion_data = scorpion_data,breadcrumbs = breadcrumbs )
     else:
        return redirect(url_for('Index'))
        
@app.route('/get_scorpion/<int:scorpion_id>', methods=['GET'])
def get_scorpion(scorpion_id):
    # Llamar a la función get_scorpion_by_id
    scorpion = get_scorpion_by_id(scorpion_id)
    if scorpion:
        return jsonify({'success': True, 'scorpion': scorpion}), 200
    else:
        return jsonify({'success': False, 'error': 'Escorpión no encontrado'}), 404

@app.route('/create_scorpion', methods=['POST'])
def create_scorpion_endpoint():
    try:
        data = request.get_json()
        if not data:
             return jsonify({"success": False, "error": "No data provided"}), 400

        scorpion_id = create_scorpion(data)

        if scorpion_id:
            return jsonify({"success": True, "scorpion_id": scorpion_id}), 201
        else:
            return jsonify({"success": False, "error": "Failed to create scorpion"}), 500

    except Exception as e:
        print(f"Error in endpoint: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/update_scorpion/<int:scorpion_id>', methods=['PUT','POST'])
def update_scorpion_endpoint(scorpion_id):
    try:

        # Si # Inicializamos un diccionario vacío para almacenar los datos
        data = {}

        # Acceder a los campos del formulario (campos de texto, select, etc.)
        for key, value in request.form.items():
            data[key] = value # no hay datos, respondemos con un error
            print(data[key] )
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        if'imagen' in request.files and request.files['imagen'].filename != '':
            imagen_final
        else:
            imagen_final = request.form.get('imagen_actual')

        # Leer todos los archivos
        for file_key, file in request.files.items():
            if file and file.filename:  # Asegura que el archivo exista
                filepath = guardar_multiples_imagenes([file], scorpion_id)
                data[file_key] = ','.join(filepath)
            else:
                return jsonify({"success": False, "error": "no se cargo la imagen"}), 500
        
        # Llamamos a la función de actualización pasando el ID y los datos
        updated_scorpion_id = update_scorpion(scorpion_id, data)

        if updated_scorpion_id:
            return jsonify({"success": True, "scorpion_id": updated_scorpion_id}), 200
        else:
            return jsonify({"success": False, "error": "Failed to update scorpion"}), 500

    except Exception as e:
        print(f"Error in update_scorpion_endpoint: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
    
@app.route('/delete_scorpioguardar_multiples_imagenesn/<int:scorpion_id>', methods=['DELETE'])
def delete_scorpion_endpoint(scorpion_id):
    try:
        # Obtener los datos en formato JSON desde la solicitud
        # Si no hay datos, respondemos con un error
        if not scorpion_id:
            return jsonify({"success": False, "error": "No data provided"}), 400
        # Llamamos a la función de actualización pasando el ID y los datos
        updated_scorpion_id = delete_scorpion(scorpion_id)

        if updated_scorpion_id:
            return jsonify({"success": True, "scorpion_id": updated_scorpion_id}), 200
        else:
            return jsonify({"success": False, "error": "Failed to update scorpion"}), 500

    except Exception as e:
        print(f"Error in update_scorpion_endpoint: {e}")
        return jsonify({"success": False, "error": str(e)}), 500



@app.route('/Contacto')
def contacto():
    return render_template('index-4.html')

@app.route('/Articulos')
@login_required 
def articulos():
     path = request.path  # obtiene la ruta actual
     breadcrumbs = build_breadcrumbs(path)
     if 'loggedin' in session and session['rol'] == "admin":
        scorpion_data = get_all_scorpions()
        return render_template('publicaciones_scorpiones.html',scorpion_data = scorpion_data,breadcrumbs = breadcrumbs )
     else:
        return redirect(url_for('Index'))


def obtener_clima_fecha(latitud, longitud, fecha, api_key_weather_api, api_key_openweather, hora=None):
    try:
        # Intentar convertir la fecha proporcionada al formato correcto
        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            try:
                fecha_obj = datetime.strptime(fecha, "%d-%m-%Y")
                fecha = fecha_obj.strftime("%Y-%m-%d")
            except ValueError:
                return {"error": "El formato de la fecha debe ser YYYY-MM-DD o DD-MM-YYYY."}

        hoy = datetime.now()

        # Verificar si la fecha no está en el futuro
        if fecha_obj > hoy:
            return {"error": "La fecha no puede estar en el futuro."}

        # Convertir la fecha al formato requerido por WeatherAPI (YYYY-MM-DD)
        fecha_str = fecha_obj.strftime("%Y-%m-%d")

        # Usar una API de geocodificación inversa para mejorar la precisión de la ubicación
        geo_url = f"https://api.bigdatacloud.net/data/reverse-geocode-client"
        geo_params = {
            "latitude": latitud,
            "longitude": longitud,
            "localityLanguage": "es"
        }
        geo_response = requests.get(geo_url, params=geo_params)
        if geo_response.status_code == 200:
            geo_data = geo_response.json()
            ubicacion = geo_data.get("locality", "Desconocida")
            region = geo_data.get("principalSubdivision", "Desconocida")
            pais = geo_data.get("countryName", "Desconocido")
        else:
            ubicacion = region = pais = "Desconocido"

        # Construir la URL para la API de WeatherAPI
        clima_url = f"https://api.weatherapi.com/v1/history.json"
        clima_params = {
            "key": api_key_weather_api,
            "q": f"{latitud},{longitud}",
            "dt": fecha_str,
            "lang": "es"
        }

        # Realizar la solicitud a la API de clima
        clima_response = requests.get(clima_url, params=clima_params)
        if clima_response.status_code == 200:
            clima_data = clima_response.json()

            # Datos generales del clima diario
            forecast = clima_data['forecast']['forecastday'][0]
            day_data = forecast['day']

            # Datos de OpenWeatherMap para altitud
            openweather_url = f"https://api.openweathermap.org/data/2.5/weather?"
            openweather_params = {
                "lat": latitud,
                "lon": longitud,
                "appid": api_key_openweather,
                "units": "metric"
            }

            openweather_response = requests.get(openweather_url, params=openweather_params)
            altitud = "No disponible"
            if openweather_response.status_code == 200:
                openweather_data = openweather_response.json()
                sea_level = openweather_data.get('main', {}).get('sea_level')
                pressure = openweather_data.get('main', {}).get('grnd_level')
                sea_level = float(sea_level)
                pressure = float(pressure)
                if sea_level and pressure:
                    try:
                        altitud_calculada = 44330 * (1 - (pressure / sea_level) ** 0.1903)
                        altitud = altitud_calculada
                    except ValueError as e:
                        altitud = "No disponible (valores inválidos de presión o nivel del mar)"
                    except Exception as e:
                        altitud = "No disponible (error inesperado)"


            # Datos por hora (si se proporciona una hora)
            clima_horario = None
            if hora:
                try:
                    hora_entera = int(hora.split(":")[0])  # Asegurarse de que hora tiene formato HH:MM
                    hora_str = f"{hora_entera:02}:00"

                    # Buscar en los datos horarios de la previsión
                    for hourly_data in forecast['hour']:
                        if hourly_data['time'].endswith(hora_str):
                            clima_horario = {
                                "temperatura": f"{hourly_data['temp_c']}°C",
                                "humedad": f"{hourly_data['humidity']}%",
                                "condiciones": hourly_data['condition']['text'],
                                "viento": f"{hourly_data['wind_kph']} km/h",
                            }
                            break
                except ValueError:
                    clima_horario = "Formato de hora inválido."

            # Construir la respuesta final
            clima = {
                "fecha": fecha,
                "ubicacion": ubicacion,
                "region": region,
                "pais": pais,
                "temperatura_max": f"{day_data['maxtemp_c']}°C",
                "temperatura_min": f"{day_data['mintemp_c']}°C",
                "humedad": f"{day_data['avghumidity']}%",
                "condiciones_dia": day_data['condition']['text'],
                "viento_max": f"{day_data['maxwind_kph']} km/h",
                "altitud": altitud,
                "clima_horario": clima_horario or "No se encontró información para la hora especificada."
            }
            return clima
        else:
            return {"error": f"No se pudo obtener el clima (HTTP {clima_response.status_code}). Verifica los datos o tu API Key."}

    except Exception as e:
        return {"error": f"Ocurrió un error: {str(e)}"}



def guardar_multiples_imagenes(imagenes, id_carpeta):
    """
    Guarda múltiples imágenes en una carpeta nombrada con el id_carpeta.
    
    Args:
        imagenes (list[FileStorage]): lista de archivos de imagen recibidos del formulario.
        id_carpeta (str or int): ID que nombra la carpeta donde guardar las imágenes.
    
    Returns:
        list[str]: lista de rutas relativas donde se guardaron las imágenes.
    """
    rutas_relativas = []
    
    # Crear carpeta si no existe
    ruta_carpeta = os.path.join(current_app.root_path, 'static/uploads', str(id_carpeta))
    os.makedirs(ruta_carpeta, exist_ok=True)
    
    for imagen in imagenes:
        # Obtener extensión segura
        extension = os.path.splitext(secure_filename(imagen.filename))[1]
        
        # Generar nombre único
        nombre_unico = f"{uuid.uuid4().hex}{extension}"
        
        # Ruta para guardar
        ruta_imagen = os.path.join(ruta_carpeta, nombre_unico)
        
        # Guardar imagen
        imagen.save(ruta_imagen)
        
        # Agregar ruta relativa
        ruta_relativa = os.path.join('static/uploads', str(id_carpeta), nombre_unico)
        rutas_relativas.append(ruta_relativa)
    
    return rutas_relativas


def get_all_users():
    try:
        connection = pool.get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios")
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(f"Error fetching users: {e}")
        return []
    finally:
        cursor.close()
        connection.close()


def get_user_by_id(user_id):
    try:
        connection = pool.get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE ID = %s", (user_id,))
        row = cursor.fetchone()
        return row
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None
    finally:
        cursor.close()
        connection.close()


def create_user(data):
    try:
        connection = pool.get_connection()
        cursor = connection.cursor()
        query = """
        INSERT INTO usuarios (nombre, apellido, correo, contrasena, rol, fecha_creacion, ultima_actualizacion)
        VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
        """
        cursor.execute(query, (data['nombre'], data['apellido'], data['correo'], data['contrasena'], data['rol']))
        connection.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error creating user: {e}")
        return None
    finally:
        cursor.close()
        connection.close()


def update_user(user_id, data):
    try:
        connection = pool.get_connection()
        cursor = connection.cursor()
        query = """
        UPDATE usuarios 
        SET nombre = %s, apellido = %s, correo = %s, contrasena = %s, rol = %s, ultima_actualizacion = NOW()
        WHERE ID = %s
        """
        cursor.execute(query, (data['nombre'], data['apellido'], data['correo'], data['contrasena'], data['rol'], user_id))
        connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error updating user: {e}")
        return False
    finally:
        cursor.close()
        connection.close()


def delete_user(user_id):
    try:
        connection = pool.get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM usuarios WHERE ID = %s", (user_id,))
        connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error deleting user: {e}")
        return False
    finally:
        cursor.close()
        connection.close()



def get_all_scorpions():
    try:
        connection = pool.get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM scorpions")
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(f"Error fetching scorpions: {e}")
        return []
    finally:
        cursor.close()
        connection.close()


def get_scorpion_by_id(scorpion_id):
    try:
        connection = pool.get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM scorpions WHERE ID = %s", (scorpion_id,))
        row = cursor.fetchone()
        print(row)
        return row
    except Exception as e:
        print(f"Error fetching scorpion by ID: {e}")
        return None
    finally:
        cursor.close()
        connection.close()


def create_scorpion(data):
    try:
        connection = pool.get_connection()
        cursor = connection.cursor()
        
        query = """
        INSERT INTO scorpions (
            orden, familia, superfamilia, subfamilia, 
            genero, subgenero, especie, descripcion, 
            Foto, Veneno, tipo, sintomas, 
            fecha_creacion, ultima_actualizacion
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
        """
        
        # Ejecutar el insert con los datos proporcionados, usando .get() con valores por defecto
        cursor.execute(query, (
            data.get('orden', ''),
            data.get('familia', ''),
            data.get('superfamilia', ''),
            data.get('subfamilia', ''),
            data.get('genero', ''),
            data.get('subgenero', ''),          # nuevo campo
            data.get('especie', ''),
            data.get('descripcion', None),      # puede ser NULL
            data.get('Foto', None),              # puede ser NULL
            data.get('veneno', ''),              # texto
            data.get('tipo', ''),                # texto
            data.get('sintomas', ''),            # texto
        ))
        
        connection.commit()

        return cursor.lastrowid
    
    except Exception as e:
        print(f"Error creating scorpion: {e}")
        return None
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def update_scorpion(scorpion_id, data):
    try:
        connection = pool.get_connection()
        cursor = connection.cursor()
        print(data)
        query = """
        UPDATE scorpions 
        SET 
            orden = %s, 
            familia = %s, 
            superfamilia = %s, 
            subfamilia = %s, 
            genero = %s, 
            subgenero = %s, 
            especie = %s, 
            descripcion = %s, 
            Foto = %s, 
            Veneno = %s, 
            tipo = %s, 
            sintomas = %s, 
            ultima_actualizacion = NOW()
        WHERE ID = %s
        """

        cursor.execute(query, (
            data.get('orden', ''),
            data.get('familia', ''),
            data.get('superfamilia', ''),
            data.get('subfamilia', ''),
            data.get('genero', ''),
            data.get('subgenero', ''),
            data.get('especie', ''),
            data.get('descripcion', None),  # puede ser NULL
            data.get('imagen', None),          # puede ser NULL
            data.get('veneno', ''),
            data.get('tipo', ''),
            data.get('sintomas', ''),
            scorpion_id
        ))

        connection.commit()

        return scorpion_id

    except Exception as e:
        print(f"Error updating scorpion: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()




def delete_scorpion(scorpion_id):
    try:
        connection = pool.get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM scorpions WHERE ID = %s", (scorpion_id,))
        connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error deleting scorpion: {e}")
        return False
    finally:
        cursor.close()
        connection.close()



def obtener_recolectas(id_scorpion=None):
    try:
        connection = pool.get_connection()
        cursor = connection.cursor(dictionary=True)

        # Consulta base
        query = """
            SELECT 
                r.ID AS recolecta_id, 
                s.ID AS scorpion_id,
                h.ID AS habitat_id,
                l.ID AS locacion_id,
                r.*, 
                c.*,
                s.*,
                h.*,
                l.*
            FROM recolecta r
            LEFT JOIN coordenadas_recolecta c ON r.ID = c.ID_recolecta
            LEFT JOIN scorpions s ON r.ID_scorpion = s.ID
            LEFT JOIN habitat h ON r.ID_habitat = h.ID
            LEFT JOIN locacion l ON r.ID_locacion = l.ID
        """

        # Agregar filtro si se proporciona un ID de escorpión
        params = ()
        if id_scorpion is not None:
            query += " WHERE r.ID_scorpion = %s"
            params = (id_scorpion,)

        cursor.execute(query, params)
        recolectas = cursor.fetchall()

        cursor.close()
        connection.close()

        return {"recolectas": recolectas}, 200

    except Exception as e:
        return {"error": str(e)}, 500
    


def obtener_recolectas_paginadas(pagina):
    try:
        # Validar que la página sea un número válido
        pagina = int(pagina) if pagina and str(pagina).isdigit() else 1
        limite = 5
        offset = (pagina - 1) * limite

        connection = pool.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Obtener recolectas paginadas con datos relacionados
        cursor.execute("""
            SELECT 
                r.*, 
                c.lat, c.longitud, c.ALT, c.humedad_ambiente, c.temperatura,
                s.nombre AS nombre_scorpion,
                h.descripcion AS descripcion_habitat,
                l.nombre AS nombre_locacion
            FROM recolecta r
            LEFT JOIN coordenadas_recolecta c ON r.ID = c.recolecta_id
            LEFT JOIN scorpion s ON r.ID_scorpion = s.ID
            LEFT JOIN habitat h ON r.ID_habitat = h.ID
            LEFT JOIN locacion l ON r.ID_locacion = l.ID
            LIMIT %s OFFSET %s
        """, (limite, offset))
        recolectas = cursor.fetchall()

        # Contar el total de recolectas
        cursor.execute("SELECT COUNT(*) AS total FROM recolecta")
        total = cursor.fetchone()["total"]

        cursor.close()
        connection.close()

        return {
            "recolectas": recolectas,
            "pagina_actual": pagina,
            "total_paginas": (total + limite - 1) // limite,
            "total_recolectas": total
        }, 200

    except Exception as e:
        return {"error": str(e)}, 500













def crear_recolecta():
    try:
        # Datos de la solicitud
        data = request.json
        fecha_captura = data['fecha_captura']
        adultomacho = data['adultomacho']
        adultohembra = data['adultohembra']
        juvenil_macho = data['juvenilmacho']
        juvenil_hembra = data['juvenilhembra']
        subadulto_macho = data['subadultomacho']
        subadulto_hembra = data['subadultohembra']
        notas = data['notas']
        id_usuario = data['id_usuario']
        id_locacion = data['id_locacion']
        id_habitat = data['id_habitat']
        id_scorpion = data['id_scorpion']
        
        # Datos para coordenadas
        lat = data['lat']
        longitud = data['longitud']
        alt = data['ALT']
        humedad_ambiente = data['humedad_ambiente']
        temperatura = data['temperatura']
        connection = pool.get_connection()
        cursor = connection.cursor(dictionary=True)

        # Insertar recolecta
        cursor.execute("""
            INSERT INTO recolecta (fecha_captura, adultomacho, adultohembra, juvenil_macho, juvenil_hembra, subadultomacho, subadultohembra, notas, ID_usuario, ID_locacion, ID_habitat, ID_scorpion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (fecha_captura, adultomacho, adultohembra, juvenil_macho, juvenil_hembra, subadulto_macho, subadulto_hembra, notas, id_usuario, id_locacion, id_habitat, id_scorpion))

        recolecta_id = cursor.lastrowid  # Obtener el ID de la recolecta insertada

        # Insertar coordenadas
        cursor.execute("""
            INSERT INTO coordenadas_recolecta (lat, longitud, ALT, humedad_ambiente, temperatura, recolecta_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (lat, longitud, alt, humedad_ambiente, temperatura, recolecta_id))

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "Recolecta y coordenadas creadas correctamente"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
def obtener_recolecta(id):
    try:
        connection = pool.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Obtener datos de la recolecta
        cursor.execute("""
            SELECT * FROM recolecta WHERE ID = %s
        """, (id,))
        recolecta = cursor.fetchone()
        
        if not recolecta:
            return {"error": "Recolecta no encontrada"}, 404

        # Obtener coordenadas relacionadas con la recolecta
        cursor.execute("""
            SELECT * FROM coordenadas_recolecta WHERE recolecta_id = %s
        """, (id,))
        coordenadas = cursor.fetchone()
        
        cursor.close()
        connection.close()

        return {
            "recolecta": recolecta,
            "coordenadas": coordenadas
        }, 200

    except Exception as e:
        return {"error": str(e)}, 500


def actualizar_recolecta(id, data):
    try:
        # Extraer datos
        fecha_captura = data['fecha_captura']
        adultomacho = data['adultomacho']
        adultohembra = data['adultohembra']
        juvenil_macho = data['juvenilmacho']
        juvenil_hembra = data['juvenilhembra']
        subadulto_macho = data['subadultomacho']
        subadulto_hembra = data['subadultohembra']
        notas = data['notas']
        id_usuario = data['id_usuario']
        id_locacion = data['id_locacion']
        id_habitat = data['id_habitat']
        id_scorpion = data['id_scorpion']
        
        # Coordenadas
        lat = data['lat']
        longitud = data['longitud']
        alt = data['ALT']
        humedad_ambiente = data['humedad_ambiente']
        temperatura = data['temperatura']

        connection = pool.get_connection()
        cursor = connection.cursor()

        # Actualizar recolecta
        cursor.execute("""
            UPDATE recolecta
            SET fecha_captura = %s, adultomacho = %s, adultohembra = %s, juvenil_macho = %s, juvenil_hembra = %s, subadultomacho = %s, subadultohembra = %s, notas = %s, ID_usuario = %s, ID_locacion = %s, ID_habitat = %s, ID_scorpion = %s
            WHERE ID = %s
        """, (fecha_captura, adultomacho, adultohembra, juvenil_macho, juvenil_hembra, subadulto_macho, subadulto_hembra, notas, id_usuario, id_locacion, id_habitat, id_scorpion, id))

        # Actualizar coordenadas
        cursor.execute("""
            UPDATE coordenadas_recolecta
            SET lat = %s, longitud = %s, ALT = %s, humedad_ambiente = %s, temperatura = %s
            WHERE recolecta_id = %s
        """, (lat, longitud, alt, humedad_ambiente, temperatura, id))

        connection.commit()
        cursor.close()
        connection.close()

        return {"message": "Recolecta y coordenadas actualizadas correctamente"}, 200

    except Exception as e:
        return {"error": str(e)}, 500




def eliminar_recolecta(id):
    connection = None
    cursor = None
    try:
        # Obtener conexión y cursor
        connection = pool.get_connection()
        cursor = connection.cursor(dictionary=True)

        # Iniciar transacción
        connection.start_transaction()

        # Eliminar coordenadas de la recolecta
        cursor.execute("""
            DELETE FROM coordenadas_recolecta WHERE ID_recolecta = %s
        """, (id,))

        # Eliminar recolecta
        cursor.execute("""
            DELETE FROM recolecta WHERE ID = %s
        """, (id,))

        # Confirmar transacción
        connection.commit()

        # Respuesta de éxito
        return {"message": "Recolecta y coordenadas eliminadas correctamente"}, 200

    except Exception as e:
        # Deshacer transacción si hay error
        if connection:
            connection.rollback()
        # Log detallado del error
        print(f"Error en eliminar_recolecta: {e}")
        # Respuesta de error
        return {"error": "Error al eliminar recolecta"}, 500

    finally:
        # Cerrar cursor y conexión
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def crear_veneno(data):
    try:
        # Extraer datos
        nombre = data['nombre']
        tipo = data['tipo']
        sintomas = data['sintomas']
        usos = data['usos']
        formula = data['formula']
        fecha_creacion = data['fecha_creacion']
        ultima_actualizacion = data['ultima_actualizacion']
        connection = pool.get_connection()
        cursor = connection.cursor()

        # Insertar veneno
        cursor.execute("""
            INSERT INTO veneno (nombre, tipo, sintomas, usos, formula, fecha_creacion, ultima_actualizacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nombre, tipo, sintomas, usos, formula, fecha_creacion, ultima_actualizacion))

        connection.commit()
        cursor.close()
        connection.close()

        return {"message": "Veneno creado correctamente"}, 201

    except Exception as e:
        return {"error": str(e)}, 500
def obtener_veneno(id):
    try:
        connection = pool.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Obtener veneno por ID
        cursor.execute("""
            SELECT * FROM veneno WHERE ID = %s
        """, (id,))
        veneno = cursor.fetchone()
        
        if not veneno:
            return {"error": "Veneno no encontrado"}, 404

        cursor.close()
        connection.close()

        return {
            "veneno": veneno
        }, 200

    except Exception as e:
        return {"error": str(e)}, 500
def actualizar_veneno(id, data):
    try:
        # Extraer datos
        nombre = data['nombre']
        tipo = data['tipo']
        sintomas = data['sintomas']
        usos = data['usos']
        formula = data['formula']
        fecha_creacion = data['fecha_creacion']
        ultima_actualizacion = data['ultima_actualizacion']

        connection = pool.get_connection()
        cursor = connection.cursor()

        # Actualizar veneno por ID
        cursor.execute("""
            UPDATE veneno
            SET nombre = %s, tipo = %s, sintomas = %s, usos = %s, formula = %s, fecha_creacion = %s, ultima_actualizacion = %s
            WHERE ID = %s
        """, (nombre, tipo, sintomas, usos, formula, fecha_creacion, ultima_actualizacion, id))

        connection.commit()
        cursor.close()
        connection.close()

        return {"message": "Veneno actualizado correctamente"}, 200

    except Exception as e:
        return {"error": str(e)}, 500

def eliminar_veneno(id):
    try:
        connection = pool.get_connection()
        cursor = connection.cursor()

        # Eliminar veneno por ID
        cursor.execute("""
            DELETE FROM veneno WHERE ID = %s
        """, (id,))

        connection.commit()
        cursor.close()
        connection.close()

        return {"message": "Veneno eliminado correctamente"}, 200

    except Exception as e:
        return {"error": str(e)}, 500



def obtener_publicaciones_por_scorpion(id_scorpion):
    try:
        connection = pool.get_connection()
        cursor = connection.cursor(dictionary=True)

        # Obtener publicaciones ligadas al ID del escorpión
        cursor.execute("""
            SELECT p.*
            FROM publicacion p
            JOIN publicacion_scorpion ps ON p.ID = ps.ID_publicacion
            WHERE ps.ID_scorpion = %s
        """, (id_scorpion,))
        
        publicaciones = cursor.fetchall()

        cursor.close()
        connection.close()

        if not publicaciones:
            return {"error": "No se encontraron publicaciones para este ID_scorpion"}, 404

        return {"publicaciones": publicaciones}, 200

    except Exception as e:
        return {"error": str(e)}, 500
def actualizar_publicacion(id, data):
    try:
        nombre = data['nombre']
        ruta = data['ruta']
        fecha_creacion = data['fecha_creacion']
        ultima_actualizacion = data['ultima_actualizacion']
        id_scorpion = data['ID_scorpion']  # No usado aquí, pero puedes usarlo si quieres actualizar también la relación

        connection = pool.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE publicacion
            SET nombre = %s, ruta = %s, fecha_creacion = %s, ultima_actualizacion = %s
            WHERE ID = %s
        """, (nombre, ruta, fecha_creacion, ultima_actualizacion, id))

        connection.commit()
        cursor.close()
        connection.close()

        return {"message": "Publicación actualizada correctamente"}, 200

    except Exception as e:
        return {"error": str(e)}, 500


def eliminar_publicacion(id):
    try:
        connection = pool.get_connection()
        cursor = connection.cursor()

        # Eliminar relación en la tabla intermedia
        cursor.execute("""
            DELETE FROM publicacion_scorpion WHERE ID_publicacion = %s
        """, (id,))

        # Eliminar la publicación
        cursor.execute("""
            DELETE FROM publicacion WHERE ID = %s
        """, (id,))

        connection.commit()
        cursor.close()
        connection.close()

        return {"message": "Publicación y relación eliminadas correctamente"}, 200

    except Exception as e:
        return {"error": str(e)}, 500
def crear_publicacion(data):
    try:
        nombre = data['nombre']
        ruta = data['ruta']
        fecha_creacion = data['fecha_creacion']
        ultima_actualizacion = data['ultima_actualizacion']
        id_scorpion = data['ID_scorpion']

        connection = pool.get_connection()
        cursor = connection.cursor()

        # Insertar publicación
        cursor.execute("""
            INSERT INTO publicacion (nombre, ruta, fecha_creacion, ultima_actualizacion)
            VALUES (%s, %s, %s, %s)
        """, (nombre, ruta, fecha_creacion, ultima_actualizacion))
        
        # Obtener el ID de la nueva publicación
        id_publicacion = cursor.lastrowid

        # Insertar relación en tabla intermedia
        cursor.execute("""
            INSERT INTO publicacion_scorpion (ID_scorpion, ID_publicacion)
            VALUES (%s, %s)
        """, (id_scorpion, id_publicacion))

        connection.commit()
        cursor.close()
        connection.close()

        return {"message": "Publicación creada y asociada correctamente"}, 201

    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == '__main__':
    app.run(debug=True)
