# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class WizChangeProductPvpManual(models.TransientModel):
    _name = "wiz.change.product.pvp.manual"
    _description = "Wizard for change in product field manual PsP"

    manual_pvp = fields.Boolean(string="Manual PSP", value=False)

    def button_change_manual_pvp(self):
        context = dict(self._context or {})
        active_ids = context.get("active_ids", []) or []
        products = self.env["product.product"].browse(active_ids)
        if products:
            products.write({"manual_pvp": self.manual_pvp})
            products._onchange_category_sale_price()
        return {"type": "ir.actions.act_window_close"}
