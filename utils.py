import os, uuid, requests
from werkzeug.utils import secure_filename
from flask import current_app
from datetime import datetime
import config

def build_breadcrumbs(path):
    parts = path.strip('/').split('/')
    breadcrumbs = []
    url = ''
    for i, part in enumerate(parts):
        url += '/' + part
        breadcrumbs.append({'name': part.capitalize(), 'url': None if i==len(parts)-1 else url})
    return breadcrumbs

def guardar_multiples_imagenes(imagenes, id_carpeta):
    rutas = []
    ruta_carpeta = os.path.join(current_app.root_path, 'static', 'uploads', str(id_carpeta))
    os.makedirs(ruta_carpeta, exist_ok=True)
    for imagen in imagenes:
        ext = os.path.splitext(secure_filename(imagen.filename))[1]
        nombre = f"{uuid.uuid4().hex}{ext}"
        ruta = os.path.join(ruta_carpeta, nombre)
        imagen.save(ruta)
        rutas.append(os.path.join('static', 'uploads', str(id_carpeta), nombre))
    return rutas

# Wrapper básico para obtener ubicación (puedes mantener tu lógica original)
def obtener_ubicacion_api(latitud, longitud):
    url = "https://revgeocode.search.hereapi.com/v1/revgeocode"
    params = {'at': f'{latitud},{longitud}', 'apikey': config.HERE_API_KEY}
    r = requests.get(url, params=params)
    if r.status_code == 200:
        data = r.json()
        if data.get('items'):
            address = data['items'][0].get('address', {})
            return {
                'pais': address.get('countryName', 'Desconocido'),
                'estado': address.get('state', 'Desconocido'),
                'municipio': address.get('city', address.get('adminLevel2', 'Desconocido')),
                'colonia': address.get('district', 'Desconocido'),
                'codigo_postal': address.get('postalCode', 'Desconocido')
            }
    return None
