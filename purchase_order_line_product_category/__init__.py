from . import models
from odoo import api, SUPERUSER_ID


def _post_install_put_categ_in_lines(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    lines = env["purchase.order.line"].search([("product_id", "!=", False)])
    for line in lines:
        line.product_categ_id = line.product_id.categ_id.id
