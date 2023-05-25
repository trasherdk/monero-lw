import monero.seed
from quart import Blueprint, redirect, request, flash, render_template
from quart_auth import login_required

from lws.models import User
from lws.helpers import lws
from lws import config


bp = Blueprint("meta", "meta")

@bp.route("/")
async def index():
    admin = User.select().first()
    if not admin:
        await flash("must setup admin first")
        return redirect("/setup")
    lws.init(admin.view_key)
    accounts = lws.list_accounts()
    del accounts["hidden"]
    requests = lws.list_requests()
    return await render_template(
        "index.html",
        config=config,
        accounts=accounts,
        requests=requests
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

