from . import models
from odoo import api, SUPERUSER_ID


def _post_install_put_last_move_locations_in_lots(cr, registry):
    """
    This method will set the production cost on already done manufacturing orders.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    lots = env["stock.lot"].search([])
    for lot in lots:
        cond = [("qty_done", ">", 0), ("state", "=", "done"), ("lot_id", "=", lot.id)]
        lines = env["stock.move.line"].search(cond)
        if lines:
            latest_line = lines.sorted(key=lambda line: line.write_date, reverse=True)[
                0
            ]
            latest_line._put_last_move_locations_in_lots()
