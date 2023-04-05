# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    update_price_on_tab = fields.Boolean(
        string="Update price on tab", default=False, copy=False,
        )

    @api.onchange("update_price_on_tab")
    def onchange_update_price_on_tab(self):
        for line in self.order_line:
            line.update_price_on_tab = self.update_price_on_tab

    @api.model
    def create(self, values):
        if ("update_price_on_tab" in values and
                values.get("update_price_on_tab", False)):
            values["update_price_on_tab"] = False
        purchase = super(PurchaseOrder, self).create(values)
        return purchase
