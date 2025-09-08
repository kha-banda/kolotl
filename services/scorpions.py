from db import get_connection

def get_all_scorpions(search_query=None, page=1, page_size=9, familia=None, genero=None, especie=None, estado=None, municipio=None):
    conn = get_connection(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SHOW COLUMNS FROM scorpions")
        columns = [r['Field'] for r in cur.fetchall()]
        base = """SELECT DISTINCT s.* FROM scorpions s
                  LEFT JOIN recolecta r ON s.ID = r.ID_scorpion
                  LEFT JOIN locacion l ON r.ID_locacion = l.ID"""
        count_q = """SELECT COUNT(DISTINCT s.ID) as total FROM scorpions s
                     LEFT JOIN recolecta r ON s.ID = r.ID_scorpion
                     LEFT JOIN locacion l ON r.ID_locacion = l.ID"""
        where = []; values = []; count_values=[]
        if search_query:
            like = f"%{search_query}%"
            clauses = [f"s.{c} LIKE %s" for c in columns] + ["l.estado LIKE %s","l.municipio LIKE %s"]
            where.append("(" + " OR ".join(clauses) + ")")
            values += [like]*len(columns) + [like, like]
            count_values = list(values)
        for k,v in (('familia',familia),('genero',genero),('especie',especie),('estado',estado),('municipio',municipio)):
            if v:
                if k in ('estado','municipio'):
                    where.append(f"l.{k} = %s"); values.append(v); count_values.append(v)
                else:
                    where.append(f"s.{k} = %s"); values.append(v); count_values.append(v)
        if where:
            where_str = " WHERE " + " AND ".join(where)
            base += where_str; count_q += where_str
        offset = (page-1)*page_size
        base += " LIMIT %s OFFSET %s"
        values += [page_size, offset]
        cur.execute(base, tuple(values))
        rows = cur.fetchall()
        # count
        cur.execute(count_q, tuple(count_values) if count_values else ())
        total = cur.fetchone()['total'] if count_values else len(rows)
        return {"results": rows, "total": total, "page": page, "page_size": page_size, "total_pages": (total + page_size -1)//page_size}
    finally:
        cur.close(); conn.close()

def get_scorpion_by_id(scorpion_id):
    conn = get_connection(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT * FROM scorpions WHERE ID = %s", (scorpion_id,))
        return cur.fetchone()
    finally:
        cur.close(); conn.close()

def create_scorpion(data):
    conn = get_connection(); cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO scorpions (orden,familia,superfamilia,subfamilia,genero,subgenero,especie,descripcion,Foto,Veneno,tipo,sintomas,fecha_creacion,ultima_actualizacion)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())
        """, (data.get('orden',''),data.get('familia',''),data.get('superfamilia',''),data.get('subfamilia',''),
              data.get('genero',''),data.get('subgenero',''),data.get('especie',''),data.get('descripcion',None),
              data.get('Foto',None),data.get('veneno',''),data.get('tipo',''),data.get('sintomas','')))
        conn.commit()
        return cur.lastrowid
    finally:
        cur.close(); conn.close()

def update_scorpion(scorpion_id, data):
    conn = get_connection(); cur = conn.cursor()
    try:
        cur.execute("""UPDATE scorpions SET orden=%s,familia=%s,superfamilia=%s,subfamilia=%s,genero=%s,subgenero=%s,especie=%s,descripcion=%s,Foto=%s,Veneno=%s,tipo=%s,sintomas=%s,ultima_actualizacion=NOW() WHERE ID=%s""",
                    (data.get('orden',''),data.get('familia',''),data.get('superfamilia',''),data.get('subfamilia',''),
                     data.get('genero',''),data.get('subgenero',''),data.get('especie',''),data.get('descripcion',None),
                     data.get('imagen',None),data.get('veneno',''),data.get('tipo',''),data.get('sintomas',''),scorpion_id))
        conn.commit()
        return scorpion_id
    finally:
        cur.close(); conn.close()

def delete_scorpion(scorpion_id):
    conn = get_connection(); cur = conn.cursor()
    try:
        cur.execute("DELETE FROM scorpions WHERE ID=%s", (scorpion_id,))
        conn.commit()
        return cur.rowcount>0
    finally:
        cur.close(); conn.close()

def get_scorpion_filters():
    conn = get_connection(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT DISTINCT familia FROM scorpions WHERE familia IS NOT NULL AND familia!=''")
        familias = [r['familia'] for r in cur.fetchall()]
        cur.execute("SELECT DISTINCT genero FROM scorpions WHERE genero IS NOT NULL AND genero!=''")
        generos = [r['genero'] for r in cur.fetchall()]
        cur.execute("SELECT DISTINCT especie FROM scorpions WHERE especie IS NOT NULL AND especie!=''")
        especies = [r['especie'] for r in cur.fetchall()]
        cur.execute("SELECT DISTINCT estado FROM locacion WHERE estado IS NOT NULL AND estado!=''")
        estados = [r['estado'] for r in cur.fetchall()]
        cur.execute("SELECT DISTINCT municipio FROM locacion WHERE municipio IS NOT NULL AND municipio!=''")
        municipios = [r['municipio'] for r in cur.fetchall()]
        return {"familias":familias,"generos":generos,"especies":especies,"estados":estados,"municipios":municipios}
    finally:
        cur.close(); conn.close()
