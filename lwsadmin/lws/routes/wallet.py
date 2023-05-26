import monero.address
from quart import Blueprint, render_template, request, flash, redirect
from quart_auth import login_required, current_user

from lws.helpers import lws


bp = Blueprint('wallet', 'wallet')


@bp.route("/wallet/add", methods=["GET", "POST"])
@login_required
async def add():
    form = await request.form
    if form:
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
        lws.add_wallet(address, view_key)
        lws.rescan(address, int(restore_height))
        await flash("wallet added")
        return redirect(f"/")
    return await render_template("wallet/add.html")


@bp.route("/wallet/rescan")
@login_required
async def rescan():
    address = request.args.get('address')
    height = request.args.get('height')
    if not address or not height:
        await flash("you need to provide both address and height")
        return redirect("/")
    if lws.rescan(address, int(height)):
        await flash(f"rescanning {address} from block {height}")
    else:
        await flash("probz")
    return redirect(f"/")


@bp.route("/wallet/<address>/disable")
@login_required
async def disable(address):
    lws.modify_wallet(address, False)
    await flash(f"{address} disabled in LWS")
    return redirect(f"/")


@bp.route("/wallet/<address>/enable")
@login_required
async def enable(address):
    lws.modify_wallet(address, True)
    await flash(f"{address} enabled in LWS")
    return redirect(f"/")

@bp.route("/wallet/<address>/accept")
@login_required
async def accept(address):
    lws.accept_request(address)
    await flash(f"{address} accepted")
    return redirect(f"/")


@bp.route("/wallet/<address>/reject")
@login_required
async def reject(address):
    lws.reject_request(address)
    await flash(f"{address} rejected")
    return redirect(f"/")

