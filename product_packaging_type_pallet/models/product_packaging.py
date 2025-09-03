# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ProductPackaging(models.Model):

    _inherit = "product.packaging"

    type_is_pallet = fields.Boolean(related="package_type_id.is_pallet")
    layers = fields.Integer()
    packs_per_layer = fields.Integer(help="number of boxes/bags on a layer")
