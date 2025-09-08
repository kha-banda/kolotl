from . import main_bp
from flask import render_template, request, session
from utils import build_breadcrumbs

@main_bp.route('/')
def index():
    path = request.path
    breadcrumbs = build_breadcrumbs(path)
    return render_template('index.html', session=session, breadcrumbs=breadcrumbs)
