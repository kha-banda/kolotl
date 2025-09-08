from . import api_bp
from flask import jsonify, request
from services.scorpions import get_scorpion_filters
from services.captures import obtener_recolectas, eliminar_recolecta
from db import get_connection

@api_bp.route('/filters', methods=['GET'])
def filters():
    return jsonify(get_scorpion_filters())

@api_bp.route('/recolectas', methods=['GET','DELETE'])
def recolectas_api():
    if request.method == 'GET':
        id_scorpion = request.args.get('id_scorpion')
        data, status = obtener_recolectas(id_scorpion)
        return jsonify(data), status
    else:
        id = request.args.get('id')
        return jsonify(*eliminar_recolecta(id))
