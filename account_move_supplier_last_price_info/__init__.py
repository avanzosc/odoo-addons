from . import models
from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    module = env["ir.module.module"].search(
        [("name", "=", "invoice_supplier_last_price_info"), ("state", "=", "installed")]
    )
    if module:
        module.button_uninstall()
        if module.state == "uninstalled":
            module.unlink()
    cond = [("last_supplier_move_id", "=", False)]
    products = env["product.product"].search(cond)
    if products:
        products.set_product_last_supplier_move()
