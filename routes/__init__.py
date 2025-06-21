# 📁 routes/__init__.py
from .main import main_bp
from .guess_who import guess_who_bp
from .discover import discover_bp
from .treasure import treasure_bp

def register_routes(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(guess_who_bp)
    app.register_blueprint(discover_bp)
    app.register_blueprint(treasure_bp)
