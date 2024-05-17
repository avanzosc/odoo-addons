from . import models
from odoo import api, SUPERUSER_ID


def _post_install_group_picking_batch_move_lines(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    pickings = env["stock.picking.batch"].search([])
    if pickings:
        pickings._compute_stock_move_line_grouped()
