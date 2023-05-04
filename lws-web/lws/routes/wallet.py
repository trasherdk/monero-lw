import monero.address
from quart import Blueprint, render_template, request, flash, redirect
from quart_auth import login_required, current_user

from lws.models import Wallet, User


bp = Blueprint('wallet', 'wallet')


@bp.route("/wallets")
@login_required
async def list():
    wallets = Wallet.select().order_by(Wallet.id.asc())
    return await render_template("wallet/list.html", wallets=wallets)

@bp.route("/wallet/add", methods=["GET", "POST"])
@login_required
async def add():
    form = await request.form
    if form:
        name = form.get("name", "")
        description = form.get("description", "")
        address = form.get("address", "")
        view_key = form.get("view_key", "")
        restore_height = form.get("restore_height", 0)
        valid_view_key = False
        if not address:
            await flash("must provide an address")
            return redirect("/wallet/add")
        if not view_key:
            await flash("must provide a view_key")
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
        return redirect(f"/wallet/{wallet.id}/rescan")
    return await render_template("wallet/add.html")


@bp.route("/wallet/<id>")
@login_required
async def show(id):
    wallet = Wallet.select().where(Wallet.id == id).first()
    if not wallet:
        await flash("wallet does not exist")
        return redirect("/wallets")
    return await render_template(
        "wallet/show.html", 
        wallet=wallet
    )

@bp.route("/wallet/<id>/rescan")
@login_required
async def rescan(id):
    wallet = Wallet.select().where(Wallet.id == id).first()
    if not wallet:
        await flash("wallet does not exist")
        return redirect("/wallets")
    wallet.rescan()
    return redirect(f"/wallet/{id}")


@bp.route("/wallet/<id>/disable")
@login_required
async def disable(id):
    wallet = Wallet.select().where(Wallet.id == id).first()
    if not wallet:
        await flash("wallet does not exist")
        return redirect("/wallets")
    wallet.disable_wallet_lws()
    return redirect(f"/wallet/{id}")

