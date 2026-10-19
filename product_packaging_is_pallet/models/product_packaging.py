# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ProductPackaging(models.Model):

    _inherit = "product.packaging"

    is_pallet = fields.Boolean(default=False)
