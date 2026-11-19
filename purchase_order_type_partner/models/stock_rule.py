# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _prepare_purchase_order(self, company_id, origins, values):
        vals = super(StockRule, self)._prepare_purchase_order(
            company_id, origins, values
        )
        if "order_type" not in vals:
            partner = self.env["res.partner"].browse(vals.get("partner_id"))
            purchase_type = (
                partner.purchase_type.id
                or partner.commercial_partner_id.purchase_type.id
            )
            if purchase_type:
                vals["order_type"] = purchase_type
        return vals
