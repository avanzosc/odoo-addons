# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class WizRecalculateProductTempSalePrice(models.TransientModel):
    _name = "wiz.recalculate.product.temp.sale.price"
    _description = "Wizard for recalculate product template sale_price"

    def button_recalculate_product_sale_price(self):
        context = dict(self._context or {})
        active_ids = context.get("active_ids", []) or []
        products = self.env["product.template"].browse(active_ids)
        if products:
            for product in products.filtered(lambda x: not x.manual_pvp):
                product._onchange_category_sale_price()
        return {"type": "ir.actions.act_window_close"}
