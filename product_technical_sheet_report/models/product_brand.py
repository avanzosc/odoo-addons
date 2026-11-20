# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductBrand(models.Model):
    _inherit = "product.brand"

    warranty_image = fields.Image()
    warranty_location = fields.Selection(
        selection=[
            ("edge", "Edge"),
            ("front_axle", "Over Front Axle"),
            ("deck", "On Deck"),
        ],
    )
    warranty_location_image = fields.Image()
