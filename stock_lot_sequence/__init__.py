from . import models
from odoo import api, SUPERUSER_ID


def _post_install_change_lot_sequence(cr, registry):
    """
    This method will set the production cost on already done manufacturing orders.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    lot_sequence = env.ref("stock.sequence_production_lots")
    lot_sequence.write(
        {
            "prefix": "A",
            "padding": 4,
            "number_next": 0,
            "number_next_actual": 1,
            "number_increment": 1,
        }
    )
