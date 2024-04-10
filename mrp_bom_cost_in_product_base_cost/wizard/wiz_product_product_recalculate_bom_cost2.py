# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class WizProductProductRecalculateBomCost2(models.TransientModel):
    _name = "wiz.product.product.recalculate.bom.cost2"
    _description = "Wizard for recalculate BoM cost in products"

    def button_recalculate_bom_cost(self):
        context = dict(self._context or {})
        active_ids = context.get("active_ids", []) or []
        products = self.env["product.product"].browse(active_ids)
        if products:
            for product in products:
                product.button_bom_cost()
        return {"type": "ir.actions.act_window_close"}
