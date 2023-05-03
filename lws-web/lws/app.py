import requests
import monero.address
from quart import Quart, render_template, redirect, request, flash, jsonify
from quart_auth import (
    AuthUser, AuthManager, login_required, login_user, logout_user, current_user, Unauthorized
)
from quart_bcrypt import Bcrypt
from quart_session import Session

from lws.models import User, Wallet
from lws import config


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


@app.route("/")
@login_required
async def index():
    admin_exists = User.select().first()
    if not admin_exists:
        return redirect("/setup")
    return await render_template("index.html")

@app.route("/debug")
async def debug():
    admin = User.get(1)
    data = {
        "auth": admin.view_key,
        "params": {
            "height": 2836540,
            "addresses": ["46pSfwbyukuduh13pqUo7R6S5W8Uk2EnqcKuPg4T9KaoHVSFQ5Qb33nBEN6xVxpeKG1TgYoxo4GxhJm2JFYN1sHJBEH1MwY"]
        }
    }
    r = requests.post("http://127.0.0.1:8081/rescan", json=data)
    return jsonify(r.json())


@app.route("/login", methods=["GET", "POST"])
async def login():
    if not User.select().first():
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
        user = User.select().where(User.username == username).first()
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


@app.route("/logout")
async def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect("/")

@app.route("/setup", methods=["GET", "POST"])
async def setup():
    if User.select().first():
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
        admin = User.create(
            username=username,
            password=pw_hash,
            address=address,
            view_key=view_key
        )
        login_user(AuthUser(admin.id))
        return redirect("/")
    return await render_template("setup.html")


@app.route("/wallet/add", methods=["GET", "POST"])
async def wallet_add():
    form = await request.form
    if form:
        name = form.get("name", "")
        description = form.get("description", "")
        address = form.get("address", "")
        view_key = form.get("view_key", "")
        restore_height = form.get("restore_height", 0)
        valid_view_key = False
        if not address:
            await flash("must provide an LWS admin address")
            return redirect("/wallet/add")
        if not view_key:
            await flash("must provide an LWS admin view_key")
            return redirect("/wallet/add")
        try:
            _a = monero.address.Address(address)
            valid_view_key = _a.check_private_view_key(view_key)
        except ValueError:
            await flash("Invalid Monero address")
            return redirect("/wallet/add")
        if not valid_view_key:
            await flash("Invalid view key provided for address")
            return redirect("/wallet/add")
        wallet = Wallet.create(
            name=name,
            description=description,
            address=address,
            view_key=view_key,
            restore_height=restore_height,
            user=User.get(current_user.auth_id)
        )
        if not name:
            wallet.name = f"wallet-{id}"
        wallet.add_wallet_lws()
        await flash("wallet added")
        return redirect(f"/wallet/{wallet.id}")
    return await render_template("wallet/add.html")


@app.route("/wallet/<id>")
@login_required
async def wallet_show(id):
    wallet = Wallet.select().where(Wallet.id == id).first()
    if not wallet:
        await flash("wallet does not exist")
        return redirect("/")
    return await render_template(
        "wallet/show.html", 
        wallet=wallet
    )

@app.route("/wallet/<id>/rescan")
@login_required
async def wallet_rescan(id):
    wallet = Wallet.select().where(Wallet.id == id).first()
    if not wallet:
        await flash("wallet does not exist")
        return redirect("/")
    wallet.rescan()
    return redirect(f"/wallet/{id}")

# / - redirect to /setup if user not setup, to /login if not authenticated
# /setup - first time setup user account, encrypted session
# /login - log into encrypted session
# /wallet/add - add a wallet to LWS
# /wallet/:id - show wallet details (balances, txes, etc)
# /wallet/:id/remove - remove a wallet from LWS
# /wallet/:id/resync - resync wallet

# get_address_info
# get_address_txs
# get_random_outs
# get_unspent_outs
# import_request
# submit_raw_tx


@app.errorhandler(Unauthorized)
async def redirect_to_login(*_):
    return redirect("/login")

def run() -> None:
    app.run()