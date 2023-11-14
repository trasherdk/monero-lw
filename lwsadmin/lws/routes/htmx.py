from quart import Blueprint, render_template, request
from monero.seed import Seed
from quart_auth import login_required

from lws.models import User, Wallet
from lws.helpers import lws
from lws import config

bp = Blueprint('htmx', 'htmx', url_prefix="/htmx")


@bp.route("/create_wallet")
async def create_wallet():
    seed = Seed()
    return await render_template(
        "htmx/create_wallet.html",
        seed=seed.phrase,
        address=seed.public_address(),
        psk=seed.public_spend_key(),
        pvk=seed.public_view_key(),
        ssk=seed.secret_spend_key(),
        svk=seed.secret_view_key()
    )

@bp.route("/import_wallet")
async def import_wallet():
    return await render_template("htmx/import_wallet.html")

@bp.route("/label_wallet")
async def label_wallet():
    address = request.args.get("address")
    label = request.args.get("label")
    return await render_template(
        "htmx/label_wallet.html", 
        address=address, 
        label=label
    )

@bp.route("/set_height")
async def set_height():
    address = request.args.get("address")
    height = request.args.get("height")
    return await render_template(
        "htmx/set_height.html",
        address=address,
        height=height
    )

@bp.route("/show_wallets")
@login_required
async def show_wallets():
    admin = User.select().first()
    lws.init(admin.view_key)
    accounts = lws.list_accounts()
    if 'hidden' in accounts:
        del accounts["hidden"]
    # make wallets if they don't exist
    for status in accounts:
        for account in accounts[status]:
            w = Wallet.select().where(Wallet.address == account["address"]).first()
            if not w:
                w = Wallet(
                    address=account["address"]
                )
                w.save()
    requests = lws.list_requests()
    return await render_template(
        "htmx/show_wallets.html",
        accounts=accounts,
        requests=requests
    )