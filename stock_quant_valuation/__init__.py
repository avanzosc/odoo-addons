from . import models
from odoo import SUPERUSER_ID
from odoo.api import Environment


def post_init_recompute(cr, registry):
    env = Environment(cr, SUPERUSER_ID, {})
    for record in env["stock.quant"].search([]):
        record.recompute_lot_fields()
    for record in env["stock.lot"].search([]):
        record.recompute_lot_values()
