from app.api.api_v1 import api_v1_blueprint
from app.api.internal.manage import manage_bp
from app.api.internal.admin import admin_bp
from app.api.routes.users import users_bp
from app.api.routes.auth import auth_bp


def register_blueprints(app):
    # Register blueprints
    app.register_blueprint(api_v1_blueprint)
    app.register_blueprint(manage_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(users_bp)
