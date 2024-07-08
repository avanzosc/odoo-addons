# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class WizGenerateAlternativeSaleCode(models.TransientModel):
    _name = "wiz.generate.alternative.sale.code"
    _description = "Wizard for generate alternative sale code in products"

    def button_generate_alternative_sale_code(self):
        context = dict(self._context or {})
        active_ids = context.get("active_ids", []) or []
        products = self.env["product.product"].browse(active_ids)
        if products:
            products.button_generate_alternative_sale_code()
        return {"type": "ir.actions.act_window_close"}
