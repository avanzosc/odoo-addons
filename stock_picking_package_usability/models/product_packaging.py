# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    packaging_length = fields.Float(string="Pack Length")
    width = fields.Float(string="Pack Width")
    height = fields.Float(string="Pack Height")
    max_weight = fields.Float()

    @api.onchange("package_type_id")
    def _onchange_package_type_id(self):
        for packaging in self:
            if packaging.package_type_id:
                package_type = packaging.package_type_id

                packaging.height = package_type.height
                packaging.width = package_type.width
                packaging.packaging_length = package_type.packaging_length

                packaging.max_weight = package_type.max_weight

    def action_open_wizard(self):
        self.ensure_one()
        return {
            "name": "Packaging",
            "type": "ir.actions.act_window",
            "res_model": "product.packaging",
            "res_id": self.id,
            "view_mode": "form",
            "views": [
                (
                    self.env.ref("product.product_packaging_form_view").id,
                    "form",
                )
            ],
            "target": "current",
        }
