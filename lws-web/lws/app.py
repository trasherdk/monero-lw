from os import environ as env
from secrets import token_urlsafe

import asyncio
import monero.address
from dotenv import load_dotenv
from quart import Quart, render_template, redirect, request, flash
from quart_auth import (
    AuthUser, AuthManager, current_user, login_required, login_user, logout_user, Unauthorized
)
from quart_bcrypt import Bcrypt
from quart_session import Session

from lws.models import Admin, Wallet

load_dotenv()


app = Quart(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["DEBUG"] = 1 == env.get("DEBUG", 1)
app.config["QUART_ENV"] = env.get("QUART_ENV", "development")
app.config["SECRET_KEY"] = env.get("SECRET_KEY", token_urlsafe(12))
app.config["SESSION_URI"] = env.get("SESSION_URI", "redis://127.0.0.1:6379")
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_PROTECTION"] = True
app.config["QUART_AUTH_DURATION"] = 60 * 60    # 1 hour
Session(app)
AuthManager(app)
bcrypt = Bcrypt(app)


@app.route("/")
@login_required
async def index():
    admin_exists = Admin.select().first()
    if not admin_exists:
        return redirect("/setup")
    return await render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
async def login():
    if not Admin.select().first():
        await flash("must setup first")
        return redirect("/setup")
    form = await request.form
    if form:
        username = form.get("username", "")
        password = form.get("password", "")
        if not username:
            await flash("must provide a username")
            return redirect("/login")
        if not password:
            await flash("must provide a password")
            return redirect("/login")
        user = Admin.select().where(Admin.username == username).first()
        if not user:
            await flash("this user does not exist")
            return redirect("/login")
        pw_matches = bcrypt.check_password_hash(user.password, password)
        if not pw_matches:
            await flash("invalid password")
            return redirect("/login")
        login_user(AuthUser(user.id))
        return redirect("/")
    return await render_template("login.html")


@app.route("/setup", methods=["GET", "POST"])
async def setup():
    if Admin.select().first():
        await flash("Setup already completed")
        return redirect("/")
    form = await request.form
    if form:
        username = form.get("username", "")
        password = form.get("password", "")
        address = form.get("address", "")
        view_key = form.get("view_key", "")
        valid_view_key = False
        if not username:
            await flash("must provide a username")
            return redirect("/setup")
        if not password:
            await flash("must provide a password")
            return redirect("/setup")
        if not address:
            await flash("must provide an LWS admin address")
            return redirect("/setup")
        if not view_key:
            await flash("must provide an LWS admin view_key")
            return redirect("/setup")
        try:
            _a = monero.address.Address(address)
            valid_view_key = _a.check_private_view_key(view_key)
        except ValueError:
            await flash("Invalid Monero address")
            return redirect("/setup")
        if not valid_view_key:
            await flash("Invalid view key provided for address")
            return redirect("/setup")
        pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        admin = Admin.create(
            username=username,
            password=pw_hash,
            address=address,
            view_key=view_key
        )
        login_user(AuthUser(admin.id))
        return redirect("/")
    return await render_template("setup.html")

# bcrypt.check_password_hash(pw_hash, "hunter2") # returns True

# / - redirect to /setup if user not setup, to /login if not authenticated
# /setup - first time setup user account, encrypted session
# /login - log into encrypted session
# /wallet/add - add a wallet to LWS
# /wallet/:id - show wallet details (balances, txes, etc)
# /wallet/:id/remove - remove a wallet from LWS
# /wallet/:id/resync - resync wallet



@app.errorhandler(Unauthorized)
async def redirect_to_login(*_):
    return redirect("/login")


# @app.get("/replay")
# async def replay():
#     data = list()
#     messages = Message.select().order_by(Message.datestamp.asc()).limit(100)
#     for m in messages:
#         data.append({
#             "message": m.message,
#             "datestamp": m.datestamp
#         })
#     return jsonify(data)


# @app.websocket("/ws")
# async def ws() -> None:
#     try:
#         task = asyncio.ensure_future(_receive())
#         async for message in broker.subscribe():
#             await websocket.send(message)
#     finally:
#         task.cancel()
#         await task


# async def _receive() -> None:
#     while True:
#         message = await websocket.receive()
#         if len(message) > 120:
#             print("too long, skipping")
#             break
#         await broker.publish(message)



def run() -> None:
    app.run()