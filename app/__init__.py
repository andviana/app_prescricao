from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.routes.prescricoes import bp as prescricoes_bp
    app.register_blueprint(prescricoes_bp, url_prefix='/prescricoes')

    from app.routes.pacientes import bp as pacientes_bp
    app.register_blueprint(pacientes_bp, url_prefix='/pacientes')

    from app.routes.internacoes import bp as internacoes_bp
    app.register_blueprint(internacoes_bp, url_prefix='/internacoes')

    from app.routes.itens import bp as itens_bp
    app.register_blueprint(itens_bp, url_prefix='/itens')

    return app
