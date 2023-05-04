import monero.seed
from quart import Blueprint, redirect, request, flash, render_template
from quart_auth import login_required

from lws.factory import bcrypt
from lws.models import Wallet, User
from lws import config


bp = Blueprint('meta', 'meta')

@bp.route("/")
@login_required
async def index():
    admin_exists = User.select().first()
    if not admin_exists:
        return redirect("/setup")
    wallets = Wallet.select().order_by(Wallet.date.desc())
    return await render_template(
        "index.html",
        config=config,
        wallets=wallets
    )


@bp.route("/utils")
async def utils():
    return await render_template("utils/index.html")


@bp.route("/utils/mnemonic", methods=["GET", "POST"])
async def utils_mnemonic():
    form = await request.form
    if form:
        seed = form.get("seed", "")
        if not seed:
            await flash("must provide mnemonic seed")
            return redirect("/utils/mnemonic")
        try:
            s = monero.seed.Seed(seed)
            return await render_template(
                "utils/mnemonic.html",
                results=s
            )
        except Exception as e:
            print(f"failed to read mnemonic seed: {e}")
            await flash("failed to parse mnemonic seed")
    return await render_template("utils/mnemonic.html")

