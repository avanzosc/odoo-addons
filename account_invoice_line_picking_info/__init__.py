from . import models
from odoo import api, SUPERUSER_ID


def _post_install_put_picking_in_lines(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    cond = [
        ("display_type", "=", "product"),
        ("move_id.move_type", "in", ("out_invoice", "out_receipt", "out_refund")),
    ]
    lines = env["account.move.line"].search(cond)
    for line in lines:
        if line.move_line_ids:
            line._put_pickings_in_line_name()
