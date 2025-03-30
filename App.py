from flask import Flask, redirect, render_template, request, url_for, session, flash
from usuarios import *  # Importa las rutas de usuarios
import mysql.connector
import time  # Importar el módulo time
import datetime 
import plotly.graph_objs as go
from functools import wraps
from flask import jsonify
from geopy.distance import geodesic
import math
from geopy.geocoders import Nominatim
import requests
from BD import *


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
        data = request.get_json()

        # Sección de Ubicación
        latitud = double(data.get('latitud'))
        longitud = data.get('longitud')
        pais = data.get('pais')
        estado = data.get('estado')
        ciudad = data.get('ciudad')
        colonia = data.get('colonia')

        # Sección de Datos Taxonómicos
        orden = data.get('orden')
        familia = data.get('familia')
        genero = data.get('genero')
        especie = data.get('especie')

        # Sección de Conteo de Alacranes
        adultos_macho = int(data.get('adultos_macho', 0))
        adultos_hembra = int(data.get('adultos_hembra', 0))
        jovenes_macho = int(data.get('jovenes_macho', 0))
        jovenes_hembra = int(data.get('jovenes_hembra', 0))
        subadultos_macho = int(data.get('subadultos_macho', 0))
        subadultos_hembra = int(data.get('subadultos_hembra', 0))
        habitat = int(data.get('habitat', 0))
        fecha_captura = data.get('fechaCaptura', '')
        notas = data.get('notas', '')
        print(fecha_captura)
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM locacion WHERE  pais = %s and estado = %s and municipio = %s and colonia  = %s ', [ pais, estado, ciudad, colonia])
        locacion = cursor.fetchone()
        # id_locacion = ""
        # if locacion:
        #      id_locacion = locacion['ID']  # Almacena el ID de la locacion
        # else:
            # cursor.execute(
            #     'INSERT INTO locacion ( cp, pais, estado, municipio, colonia, fecha_creacion, ultima_actualizacion) VALUES (%s,%s,%s,%s,%s, NOW(), NOW())',
            #     (" ",pais,estado,ciudad,colonia)

            # )
            # connection.commit()
            # # Obtener el ID del registro insertado
            # id_locacion = cursor.lastrowid
        # cursor.execute('SELECT * FROM scorpions WHERE  orden = %s and familia = %s and genero = %s and especie  = %s ', [orden, familia, genero, especie])
        # scorpion = cursor.fetchone()
        # id_scorpion = ""
        # if scorpion:
        #     id_scorpion = scorpion['ID']
        # else:
        #     return jsonify({'error':' escorpion no encontrado.'}), 500
    
        temperatura= obtener_clima_fecha(latitud,longitud,fecha_captura,API_KEY)
        print(temperatura)
        connection.commit()

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
        adultos_macho = int(request.form.get('adultos_macho', 0))
        adultos_hembra = int(request.form.get('adultos_hembra', 0))
        jovenes_macho = int(request.form.get('jovenes_macho', 0))
        jovenes_hembra = int(request.form.get('jovenes_hembra', 0))
        subadultos_macho = int(request.form.get('subadultos_macho', 0))
        subadultos_hembra = int(request.form.get('subadultos_hembra', 0))
        habitat = int(request.form.get('habitat', 0))
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
                'lat': row['lat'],
                'longitud': row['longitud'],
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
        
        # Imprimir la respuesta completa para verificar su estructura
        print("Respuesta de HERE API:", data)

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
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
        SELECT 
            s.*,        -- Todos los campos de la tabla scorpions con prefijo s
            v.*,        -- Todos los campos de la tabla veneno con prefijo v
            mp.*,       -- Todos los campos de la tabla multiples_publicaciones con prefijo mp
            p.*         -- Todos los campos de la tabla publicaciones con prefijo p
        FROM scorpions s
        LEFT JOIN veneno v ON s.ID_veneno = v.ID
        LEFT JOIN publicacion_scorpion mp ON s.ID = mp.ID_scorpion
        LEFT JOIN publicacion p ON mp.ID_publicacion = p.ID
        """)
        scorpion_data = cursor.fetchall()




        return render_template('scorpions.html',scorpion_data = scorpion_data )
     else:
        return redirect(url_for('Index'))








@app.route('/Contacto')
def contacto():
    return render_template('index-4.html')







def obtener_clima_fecha(latitud, longitud, fecha, api_key_weather_api):
    try:
        # Intentar convertir la fecha proporcionada al formato correcto
        try:
            fecha_obj = datetime.datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            try:
                # Intentar con formatos comunes incorrectos
                fecha_obj = datetime.datetime.strptime(fecha, "%d-%m-%Y")
                # Si se corrige el formato, cambiar a YYYY-MM-DD
                fecha = fecha_obj.strftime("%Y-%m-%d")
            except ValueError:
                return {"error": "El formato de la fecha debe ser YYYY-MM-DD o DD-MM-YYYY."}

        hoy = datetime.datetime.now()

        # Verificar si la fecha no está en el futuro
        if fecha_obj > hoy:
            return {"error": "La fecha no puede estar en el futuro."}

        # Convertir la fecha al formato requerido por WeatherAPI (YYYY-MM-DD)
        fecha_str = fecha_obj.strftime("%Y-%m-%d")

        # Construir la URL para la API de WeatherAPI
        url = f"https://api.weatherapi.com/v1/history.json"
        params = {
            "key": api_key_weather_api,
            "q": f"{latitud},{longitud}",
            "dt": fecha_str,
            "lang": "es"
        }

        # Realizar la solicitud a la API
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()

            # Construir la respuesta con los datos relevantes
            altitud = None
            if "main" in data and "sea_level" in data["main"] and "grnd_level" in data["main"]:
                presion_nivel_mar = data["main"]["sea_level"]
                presion_suelo = data["main"]["grnd_level"]
                # Fórmula simplificada para calcular altitud
                altitud = 44330 * (1 - (presion_suelo / presion_nivel_mar) ** 0.1903)
            clima = {
                "fecha": fecha,
                "ubicacion": data['location']['name'],
                "region": data['location']['region'],
                "pais": data['location']['country'],
                "temperatura_max": f"{data['forecast']['forecastday'][0]['day']['maxtemp_c']}°C",
                "temperatura_min": f"{data['forecast']['forecastday'][0]['day']['mintemp_c']}°C",
                "humedad": f"{data['forecast']['forecastday'][0]['day']['avghumidity']}%",
                "condiciones": data['forecast']['forecastday'][0]['day']['condition']['text'],
                "viento_max": f"{data['forecast']['forecastday'][0]['day']['maxwind_kph']} km/h",
                "altitud": f"{altitud:.2f} metros" if altitud else "No disponible"
            }
            return clima
        else:
            return {"error": "No se pudo obtener el clima. Verifica los datos o tu API Key."}

    except ValueError as e:
        return {"error": f": {str(e)}"}


if __name__ == '__main__':
    app.run(debug=True)
