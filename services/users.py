from db import get_connection

def get_all_users():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT * FROM usuarios")
        return cur.fetchall()
    finally:
        cur.close(); conn.close()

def get_user_by_id(user_id):
    conn = get_connection(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT * FROM usuarios WHERE ID = %s", (user_id,))
        return cur.fetchone()
    finally:
        cur.close(); conn.close()

def create_user(data):
    conn = get_connection(); cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO usuarios (nombre, apellido, correo, contrasena, rol, fecha_creacion, ultima_actualizacion)
            VALUES (%s,%s,%s,%s,%s,NOW(),NOW())
        """, (data['nombre'], data['apellido'], data['correo'], data['contrasena'], data['rol']))
        conn.commit()
        return cur.lastrowid
    finally:
        cur.close(); conn.close()

def update_user(user_id, data):
    conn = get_connection(); cur = conn.cursor()
    try:
        cur.execute("UPDATE usuarios SET nombre=%s, apellido=%s, correo=%s, contrasena=%s, rol=%s, ultima_actualizacion=NOW() WHERE ID=%s",
                    (data['nombre'], data['apellido'], data['correo'], data['contrasena'], data['rol'], user_id))
        conn.commit()
        return cur.rowcount>0
    finally:
        cur.close(); conn.close()

def delete_user(user_id):
    conn = get_connection(); cur = conn.cursor()
    try:
        cur.execute("DELETE FROM usuarios WHERE ID=%s", (user_id,))
        conn.commit()
        return cur.rowcount>0
    finally:
        cur.close(); conn.close()
