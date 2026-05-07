# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    lot_code = fields.Char()
