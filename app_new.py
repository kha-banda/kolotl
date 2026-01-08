from flask import Flask
import config
from db import init_pool
from blueprints.main import main_bp
from blueprints.scorpions import scorpions_bp
from blueprints.api import api_bp

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER

    # Inicializar pool DB
    init_pool()

    # Registrar blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(scorpions_bp)
    app.register_blueprint(api_bp)

    # Opcional: registrar otros blueprints (auth, captures) si los creas
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
