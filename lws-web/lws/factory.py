from quart import Quart, redirect
from quart_auth import (
    AuthManager, Unauthorized
)
from quart_bcrypt import Bcrypt
from quart_session import Session

from lws import config


def create_app():
    app = Quart(__name__)
    app.config["TEMPLATES_AUTO_RELOAD"] = config.TEMPLATES_AUTO_RELOAD
    app.config["DEBUG"] = config.DEBUG
    app.config["QUART_ENV"] = config.QUART_ENV
    app.config["SECRET_KEY"] = config.SECRET_KEY
    app.config["SESSION_URI"] = config.SESSION_URI
    app.config["SESSION_TYPE"] = config.SESSION_TYPE
    app.config["SESSION_PROTECTION"] = config.SESSION_PROTECTION
    app.config["QUART_AUTH_DURATION"] = config.QUART_AUTH_DURATION
    Session(app)
    AuthManager(app)
    bcrypt = Bcrypt(app)
    
    @app.before_serving
    async def startup():
        from lws.routes import auth, wallet, meta
        from lws import filters
        app.register_blueprint(filters.bp)
        app.register_blueprint(auth.bp)
        app.register_blueprint(meta.bp)
        app.register_blueprint(wallet.bp)

    @app.errorhandler(Unauthorized)
    async def redirect_to_login(*_):
        return redirect("/login")
    return app
    
bcrypt = Bcrypt(create_app())