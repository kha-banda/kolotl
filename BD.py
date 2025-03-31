import mysql.connector
from mysql.connector import pooling
import os

# Configuración del pool de conexiones
pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    host='69.62.71.171',
    user='root',
    password='caravanadestrucs',
    database='scorpions'
)


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
        INSERT INTO scorpions (orden, familia, superfamilia, subfamilia, genero, especie, descripcion, ID_veneno, fecha_creacion, ultima_actualizacion)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
        """
        
        # Usa `.get(clave, valor_por_defecto)` para manejar valores faltantes
        cursor.execute(query, (
            data.get('orden', ''), 
            data.get('familia', ''), 
            data.get('superfamilia', ''), 
            data.get('subfamilia', ''), 
            data.get('genero', ''), 
            data.get('especie', ''), 
            data.get('descripcion', ''),  # Si no existe, se guarda como vacío
            data.get('ID_veneno', None)  # Si no existe, se guarda como NULL
        ))

        # Confirma la transacción
        connection.commit()

        # Devuelve el ID del último registro insertado
        return cursor.lastrowid
    
    except Exception as e:
        print(f"Error creating scorpion: {e}")
        return None
    
    finally:
        if cursor:
            cursor.close()  # Cierra el cursor
        if connection:
            connection.close()  # Cierra la conexión



def update_scorpion(scorpion_id, data):
    try:
        # Obtener conexión a la base de datos
        connection = pool.get_connection()
        cursor = connection.cursor()

        # Actualizar la consulta para modificar los valores del escorpión
        query = """
        UPDATE scorpions 
        SET orden = %s, 
            familia = %s, 
            superfamilia = %s, 
            subfamilia = %s, 
            genero = %s, 
            especie = %s, 
            descripcion = %s, 
            ID_veneno = %s, 
            ultima_actualizacion = NOW()
        WHERE id = %s
        """
        
        # Ejecutar la consulta con los datos proporcionados
        cursor.execute(query, (
            data.get('orden', ''),
            data.get('familia', ''),
            data.get('superfamilia', ''),
            data.get('subfamilia', ''),
            data.get('genero', ''),
            data.get('especie', ''),
            data.get('descripcion', ''),
            data.get('ID_veneno', None),  # Si no existe, se guarda como NULL
            scorpion_id
        ))

        # Confirmar la transacción
        connection.commit()

        # Devolver el ID del escorpión actualizado
        return scorpion_id

    except Exception as e:
        print(f"Error updating scorpion: {e}")
        return None

    finally:
        if cursor:
            cursor.close()  # Cerrar el cursor
        if connection:
            connection.close()  # Cerrar la conexión



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



def obtener_todas_recolectas():
    try:
        connection = pool.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Obtener todas las recolectas con datos relacionados
        cursor.execute("""
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
        """)
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

        conn.commit()
        cursor.close()
        conn.close()

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
        conn.close()

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

        conn = get_db_connection()
        cursor = conn.cursor()

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

        conn.commit()
        cursor.close()
        conn.close()

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

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insertar veneno
        cursor.execute("""
            INSERT INTO veneno (nombre, tipo, sintomas, usos, formula, fecha_creacion, ultima_actualizacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nombre, tipo, sintomas, usos, formula, fecha_creacion, ultima_actualizacion))

        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Veneno creado correctamente"}, 201

    except Exception as e:
        return {"error": str(e)}, 500
def obtener_veneno(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Obtener veneno por ID
        cursor.execute("""
            SELECT * FROM veneno WHERE ID = %s
        """, (id,))
        veneno = cursor.fetchone()
        
        if not veneno:
            return {"error": "Veneno no encontrado"}, 404

        cursor.close()
        conn.close()

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

        conn = get_db_connection()
        cursor = conn.cursor()

        # Actualizar veneno por ID
        cursor.execute("""
            UPDATE veneno
            SET nombre = %s, tipo = %s, sintomas = %s, usos = %s, formula = %s, fecha_creacion = %s, ultima_actualizacion = %s
            WHERE ID = %s
        """, (nombre, tipo, sintomas, usos, formula, fecha_creacion, ultima_actualizacion, id))

        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Veneno actualizado correctamente"}, 200

    except Exception as e:
        return {"error": str(e)}, 500

def eliminar_veneno(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Eliminar veneno por ID
        cursor.execute("""
            DELETE FROM veneno WHERE ID = %s
        """, (id,))

        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Veneno eliminado correctamente"}, 200

    except Exception as e:
        return {"error": str(e)}, 500



def crear_publicacion(data):
    try:
        # Extraer datos
        nombre = data['nombre']
        ruta = data['ruta']
        fecha_creacion = data['fecha_creacion']
        ultima_actualizacion = data['ultima_actualizacion']
        id_scorpion = data['ID_scorpion']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insertar publicación
        cursor.execute("""
            INSERT INTO publicacion (nombre, ruta, fecha_creacion, ultima_actualizacion, ID_scorpion)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, ruta, fecha_creacion, ultima_actualizacion, id_scorpion))

        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Publicación creada correctamente"}, 201

    except Exception as e:
        return {"error": str(e)}, 500

def obtener_publicacion(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Obtener publicación por ID
        cursor.execute("""
            SELECT * FROM publicacion WHERE ID = %s
        """, (id,))
        publicacion = cursor.fetchone()
        
        if not publicacion:
            return {"error": "Publicación no encontrada"}, 404

        cursor.close()
        conn.close()

        return {
            "publicacion": publicacion
        }, 200

    except Exception as e:
        return {"error": str(e)}, 500
def actualizar_publicacion(id, data):
    try:
        # Extraer datos
        nombre = data['nombre']
        ruta = data['ruta']
        fecha_creacion = data['fecha_creacion']
        ultima_actualizacion = data['ultima_actualizacion']
        id_scorpion = data['ID_scorpion']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Actualizar publicación por ID
        cursor.execute("""
            UPDATE publicacion
            SET nombre = %s, ruta = %s, fecha_creacion = %s, ultima_actualizacion = %s, ID_scorpion = %s
            WHERE ID = %s
        """, (nombre, ruta, fecha_creacion, ultima_actualizacion, id_scorpion, id))

        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Publicación actualizada correctamente"}, 200

    except Exception as e:
        return {"error": str(e)}, 500
def eliminar_publicacion(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Eliminar publicación por ID
        cursor.execute("""
            DELETE FROM publicacion WHERE ID = %s
        """, (id,))

        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Publicación eliminada correctamente"}, 200

    except Exception as e:
        return {"error": str(e)}, 500
