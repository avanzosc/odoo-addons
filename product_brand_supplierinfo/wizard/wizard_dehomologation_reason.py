# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class WizardDehomologationReason(models.TransientModel):
    _name = "wizard.dehomologation.reason"
    _description = "Wizard Dehomologation Reason"

    brand_product_id = fields.Many2one(
        string="Brand Product",
        comodel_name="brand.product",
    )
    dehomologation_reason = fields.Text(required=True)

    def default_get(self, fields):
        result = super().default_get(fields)
        if "active_id" in self.env.context:
            result["brand_product_id"] = self.env.context.get("active_id")
        return result

    def change_dehomologation_reason(self):
        self.brand_product_id.write(
            {
                "dehomologation_reason": self.dehomologation_reason,
                "dehomologation_date": fields.Date.context_today(self),
                "state": "dehomologation",
            }
        )
