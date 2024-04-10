# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class WizProductTemplateRecalculateBomCost(models.TransientModel):
    _name = "wiz.product.template.recalculate.bom.cost"
    _description = "Wizard for recalculate BoM cost in products"

    def button_recalculate_bom_cost(self):
        context = dict(self._context or {})
        active_ids = context.get("active_ids", []) or []
        templates = self.env["product.template"].browse(active_ids)
        if templates:
            for template in templates:
                template.action_bom_cost()
        return {"type": "ir.actions.act_window_close"}
