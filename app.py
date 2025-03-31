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
from BD import *
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

# Tu clave de API de HERE
HERE_API_KEY = '1F91LCxBz_coxRzfxs5qybZKq0a-09Q40EyQMsP_ehA'
OPEN_WEATHER_MAP = '0c92193205b8016c9c0cedc51ebd650b'
app.secret_key = 'kolotl_unca'  # Necesario para gestionar sesiones

# Tu API Key de OpenWeatherMap
API_KEY = "ec66f746a0e14f57ac1152001242911"
# Conexión a la base de datos MySQL usando mysql-connector
connection = mysql.connector.connect(
    host='69.62.71.171',
    user='root',
    password='caravanadestrucs',
    database='scorpions'
)

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
    if 'loggedin' in session:
        return render_template('index.html',session = session )
    else:
        return render_template('index.html')


###################################################################     
#usuarios-admin                                                   #
###################################################################
@app.route('/Usuarios')
@login_required  # Esto asegura que solo usuarios autenticados puedan acceder a esta ruta
def users():
     if 'loggedin' in session and session['rol'] == "admin":
        
        usuarios = get_all_users()
        return render_template('users.html',session = session,usuarios = usuarios )
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
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM usuarios WHERE ID = %s', [id])
    usuario = cursor.fetchone()
    
    if usuario:
        return jsonify(usuario)
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404
# Ruta para actualizar un usuario existente
@app.route('/actualizar_usuario/<int:id>', methods=['POST'])
@login_required
def actualizar_usuario(id):
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
    if cursor.rowcount > 0:
        return jsonify({'success': True})
    return jsonify({'error': 'Usuario no encontrado'}), 404
# Ruta para eliminar un usuario
@app.route('/eliminar_usuario/<int:id>', methods=['POST'])
@login_required
def eliminar_usuario(id):
    cursor = connection.cursor(dictionary=True)
    cursor.execute('DELETE FROM usuarios WHERE id = %s', [id])
    connection.commit()
    if cursor.rowcount > 0:
        return jsonify({'success': True})
    return jsonify({'error': 'Usuario no encontrado'}), 404




@app.route('/capturas')
def capturas():
    if 'loggedin' in session:
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

        return render_template('capturas.html',session = session,scorpiones = scorpion_data,habitats = habitats )
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


        return jsonify({'success': 'Datos guardados correctamente.'}), 200
    except Exception as e:
        print(f"Error al procesar los datos: {e}")
        return jsonify({'error': 'Hubo un error al procesar los datos.'}), 500

@app.route('/actualizar_captura', methods=['POST'])
@login_required
def actualizar_captura():
    try:
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

        return jsonify({'success': 'Datos actualizados correctamente.'}), 200
    except Exception as e:
        print(f"Error al procesar los datos: {e}")
        return jsonify({'error': 'Hubo un error al procesar los datos.'}), 500



@app.route('/get_captures', methods=['GET'])
def get_captures():
    try:
        # Llama a la función y desestructura los datos y el código HTTP
        data, status_code = obtener_todas_recolectas()
        return jsonify(data), status_code
    except Exception as e:
        print(f"Error retrieving captures: {e}")
        return jsonify({'error': 'Failed to retrieve capture data.'}), 500


@app.route('/get_captures_data', methods=['GET'])
def get_captures_data():
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Recuperar detalles de las capturas
        cursor.execute("SELECT * FROM recolecta")
        capturas = cursor.fetchall()

        # Inicializar estadísticas
        total_captures = len(capturas)
        total_scorpions = sum(row['adultomacho'] + row['adultohembra'] + row['juvenilmacho'] + row['juvenilhembra']
                              + row['subadultomacho'] + row['subadultohembra'] for row in capturas)
        
        habitats_count = {}
        species_count = {}

        captures = []

        for row in capturas:
            # Consultas optimizadas para obtener los datos relacionados con cada captura
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

            # Asignar los valores recuperados
            habitat_name = result['habitat_name'] if result['habitat_name'] else 'Unknown'
            species_name = result['species_name'] if result['species_name'] else 'Unknown'
            species_family = result['species_family'] if result['species_family'] else 'Unknown'
            species_genero = result['species_genero'] if result['species_genero'] else 'Unknown'
            locacion = {'estado': result['estado'], 'municipio': result['municipio']}
            persona = {'nombre': result['usuario_nombre'], 'apellido': result['usuario_apellido']}

            # Contabilizar los hábitats y las especies
            habitats_count[habitat_name] = habitats_count.get(habitat_name, 0) + 1
            species_count[species_name] = species_count.get(species_name, 0) + 1

            # Agregar la captura a la lista
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

        # Responder con las capturas y estadísticas
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
        # Obtén los datos del formulario
        email = request.form['email']
        password = request.form['password']
        
        # Verifica las credenciales en la base de datos
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios WHERE correo = %s AND contrasena = %s', (email, password))
        user = cursor.fetchone()
        
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
        rol_var = request.form['ID']
        correo_var = request.form['Email']
        name_var = request.form['Nombre']
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (role_id, email, first_name) VALUES (%s, %s, %s)', (rol_var, correo_var, name_var))
        connection.commit()
        flash('Contacto añadido exitosamente!', 'success')
        return redirect(url_for('Index'))

# Ruta para eliminar un contacto (ejemplo de eliminación de la base de datos)
@app.route('/delete_contact/<string:id>')
def delete_contact(id):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM users WHERE id = %s', (id,))
    connection.commit()
    flash('Contacto eliminado exitosamente!', 'success')
    return redirect(url_for('Index'))

# Ruta para visualizar estadísticas (ejemplo de gráficos con Plotly)
@app.route('/Estadisticas')
@login_required
def estadisticas():
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

    return render_template('estadisticas.html', graphJSON=graph_json, graph2JSON=graph2_json, data_barras=data_barras)

# Rutas adicionales de la página
@app.route('/Galeria')
def galeria():
    return render_template('index-2.html')

@app.route('/map')
def map():
    return render_template('map.html')
@app.route('/Acerca')
def acerca():
    return render_template('index-3.html')


@app.route('/scorpiones')
@login_required  # Esto asegura que solo usuarios autenticados puedan acceder a esta ruta
def scorpiones():
     if 'loggedin' in session and session['rol'] == "admin":
        scorpion_data = get_all_scorpions()
        return render_template('scorpions.html',scorpion_data = scorpion_data )
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

@app.route('/update_scorpion/<int:scorpion_id>', methods=['PUT'])
def update_scorpion_endpoint(scorpion_id):
    try:
        # Obtener los datos en formato JSON desde la solicitud
        data = request.get_json()
        
        # Si no hay datos, respondemos con un error
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        # Llamamos a la función de actualización pasando el ID y los datos
        updated_scorpion_id = update_scorpion(scorpion_id, data)

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




if __name__ == '__main__':
    app.run(debug=True)
