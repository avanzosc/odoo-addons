# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    account_payment_ids = fields.One2many(
        string="Account Payments",
        comodel_name="account.payment",
        inverse_name="picking_id",
    )

    def action_view_payments(self):
        context = self.env.context.copy()
        context.update({"default_picking_id": self.id})
        return {
            "name": _("Account Payments"),
            "view_mode": "tree,form",
            "res_model": "account.payment",
            "domain": [("id", "in", self.account_payment_ids.ids)],
            "type": "ir.actions.act_window",
            "context": context,
        }
