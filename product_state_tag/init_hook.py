# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    cond = [('first_state', '=', True)]
    first_state = env['product.state'].search(cond, limit=1)
    products = env['product.product'].search([])
    if products:
        products.write({'state_id': first_state.id})
