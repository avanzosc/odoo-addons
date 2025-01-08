from . import models
from odoo import api, SUPERUSER_ID


def _post_install_active_product_brand(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    brands = env["product.brand"].search([])
    if brands:
        brands.write({"active": True})
