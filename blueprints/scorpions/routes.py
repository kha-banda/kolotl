from . import scorpions_bp
from flask import render_template, request
from services.scorpions import get_all_scorpions, get_scorpion_filters, get_scorpion_by_id

@scorpions_bp.route('/')
def galeria():
    path = request.path
    search = request.args.get('search')
    familia = request.args.get('familia')
    genero = request.args.get('genero')
    especie = request.args.get('especie')
    estado = request.args.get('estado')
    municipio = request.args.get('municipio')
    page = int(request.args.get('page', 1))
    data = get_all_scorpions(search_query=search, familia=familia, genero=genero, especie=especie, estado=estado, municipio=municipio, page=page)
    filtros = get_scorpion_filters()
    return render_template('index-2.html', scorpion_data=data['results'], total=data['total'], current_page=data['page'], total_pages=data['total_pages'], search=search, familias=filtros['familias'], generos=filtros['generos'], especies=filtros['especies'], estados=filtros['estados'], municipios=filtros['municipios'], familia=familia, genero=genero, especie=especie, estado=estado, municipio=municipio)

@scorpions_bp.route('/Escorpion/')
def galeria_escorpion():
    id_scorpion = request.args.get('id_scorpion')
    scorpion_data = get_scorpion_by_id(id_scorpion)
    return render_template('escorpion.html', scorpion_data=scorpion_data)
