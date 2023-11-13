import monero.address
from quart import Blueprint, render_template, request, flash, redirect, url_for
from quart_auth import login_required, current_user

from lws.helpers import lws
from lws.models import Wallet, get_random_words


bp = Blueprint("wallet", "wallet")


@bp.route("/wallet/add", methods=["GET", "POST"])
@login_required
async def add():
    form = await request.form
    if form:
        label = form.get("label")
        address = form.get("address", "")
        view_key = form.get("view_key", "")
        restore_height = form.get("restore_height", None)
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
        lws.add_wallet(address, view_key)
        if restore_height != "-1":
            lws.rescan(address, int(restore_height))
        w = Wallet(
            address=address,
            view_key=view_key,
            label=label if label else get_random_words()
        )
        w.save()
        await flash("wallet added")
        return redirect(f"/")
    else:
        return ""


@bp.route("/wallet/rescan")
@login_required
async def rescan():
    address = request.args.get("address")
    height = request.args.get("height")
    if not address or not height:
        await flash("you need to provide both address and height")
        return redirect("/")
    if lws.rescan(address, int(height)):
        await flash(f"rescanning {address} from block {height}")
    else:
        await flash("probz")
    return redirect(f"/")


@bp.route("/wallet/<address>/<status>")
@login_required
async def modify(address, status):
    lws.modify_wallet(address, status)
    await flash(f"{address} {status} in LWS")
    return redirect(url_for("htmx.show_wallets"))


@bp.route("/wallet/<address>/approve")
@login_required
async def accept(address):
    lws.accept_request(address)
    await flash(f"{address} accepted")
    return redirect(url_for("htmx.show_wallets"))


@bp.route("/wallet/<address>/deny")
@login_required
async def reject(address):
    lws.reject_request(address)
    await flash(f"{address} denied")
    return redirect(url_for("htmx.show_wallets"))


@bp.route("/wallet/<address>/label/<label>")
@login_required
async def label(address, label):
    w = Wallet.select().where(Wallet.address == address).first()
    if w and label:
        w.label = label
        w.save()
    return redirect(url_for("htmx.show_wallets"))
