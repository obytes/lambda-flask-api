from app.api.api_v1 import api_v1_blueprint
from app.api.manage.routes import manage_bp
from app.api.admins.routes import admins_bp
from app.api.users.routes import users_bp


def register_blueprints(app):
    # Register blueprints
    app.register_blueprint(api_v1_blueprint)
    app.register_blueprint(manage_bp)
    app.register_blueprint(admins_bp)
    app.register_blueprint(users_bp)
