# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockPackageType(models.Model):
    _inherit = "stock.package.type"

    is_pallet = fields.Boolean()
