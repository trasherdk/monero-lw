from monero.numbers import from_atomic
from quart import Blueprint


bp = Blueprint('filters', 'filters')


@bp.app_template_filter('atomic')
def atomic(amt):
    return float(from_atomic(amt))
