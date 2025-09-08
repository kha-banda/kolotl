from db import get_connection

def obtener_recolectas(id_scorpion=None):
    conn = get_connection(); cur = conn.cursor(dictionary=True)
    try:
        q = """
            SELECT r.*, c.*, s.familia, s.genero, s.especie, h.nombre AS habitat_name, l.estado, l.municipio, u.nombre AS usuario_nombre, u.apellido AS usuario_apellido
            FROM recolecta r
            LEFT JOIN coordenadas_recolecta c ON r.ID = c.ID_recolecta
            LEFT JOIN scorpions s ON r.ID_scorpion = s.ID
            LEFT JOIN habitat h ON r.ID_habitat = h.ID
            LEFT JOIN locacion l ON r.ID_locacion = l.ID
            LEFT JOIN usuarios u ON r.ID_usuario = u.ID
        """
        params = ()
        if id_scorpion is not None:
            q += " WHERE r.ID_scorpion = %s"; params = (id_scorpion,)
        cur.execute(q, params)
        recolectas = cur.fetchall()
        return {"recolectas": recolectas}, 200
    finally:
        cur.close(); conn.close()

def eliminar_recolecta(id):
    conn = get_connection(); cur = conn.cursor(dictionary=True)
    try:
        conn.start_transaction()
        cur.execute("DELETE FROM coordenadas_recolecta WHERE ID_recolecta = %s", (id,))
        cur.execute("DELETE FROM recolecta WHERE ID = %s", (id,))
        conn.commit()
        return {"message":"ok"}, 200
    except Exception as e:
        if conn: conn.rollback()
        return {"error":str(e)}, 500
    finally:
        cur.close(); conn.close()
