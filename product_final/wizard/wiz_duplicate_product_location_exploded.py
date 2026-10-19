# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class WizDuplicateProductLocationExploded(models.TransientModel):
    _name = "wiz.duplicate.product.location.exploded"
    _description = "Wizard For Duplicate Products Exploded Locations"

    product_final_id = fields.Many2one(
        comodel_name="product.final",
        string="Final Product",
        required=True,
    )
    view_version_id = fields.Many2one(
        string="View version", comodel_name="product.final.view.version", required=True
    )
    product_list_version_id = fields.Many2one(
        string="Product List Version",
        comodel_name="product.final.product.list.version",
        required=True,
    )

    def button_duplicate_product_location_exploded(self):
        self.ensure_one()
        plexplodeds = self.env["product.location.exploded"].browse(
            self.env.context.get("active_ids")
        )
        for plexploded in plexplodeds:
            plexploded.copy(
                default={
                    "product_final_id": self.product_final_id.id,
                    "view_version_id": self.view_version_id.id,
                    "product_list_version_id": self.product_list_version_id.id,
                }
            )
