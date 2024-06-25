# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockPickingImport(models.Model):
    _inherit = "stock.picking.import"

    data = fields.Binary(required=False)
