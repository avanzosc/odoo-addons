# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def action_bom_cost(self):
        return super(
            ProductProduct, self.with_context(update_base_cost=True)
        ).action_bom_cost()

    def button_bom_cost(self):
        self.ensure_one()
        return super(
            ProductProduct, self.with_context(update_base_cost=True)
        ).button_bom_cost()

    def do_change_standard_price(self, new_price, account_id):
        result = super(
            ProductProduct, self.with_context(update_base_cost=True)
        ).do_change_standard_price(new_price, account_id)
        return result

    def button_call_wizard_calculate_bom_cost(self):
        self.ensure_one()
        wiz_obj = self.env["wiz.product.product.recalculate.bom.cost2"]
        wiz = wiz_obj.with_context(
            {
                "active_id": self.id,
                "active_ids": self.ids,
                "active_model": "product.product",
            }
        ).create({})
        context = self.env.context.copy()
        context.update(
            {
                "active_id": self.id,
                "active_ids": self.ids,
                "active_model": "product.product",
            }
        )
        return {
            "name": _("Recalculate BoM cost in products"),
            "type": "ir.actions.act_window",
            "res_model": "wiz.product.product.recalculate.bom.cost2",
            "view_type": "form",
            "view_mode": "form",
            "res_id": wiz.id,
            "target": "new",
            "context": context,
        }
