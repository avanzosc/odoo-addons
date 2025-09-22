# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    partner_id = fields.Many2one(
        string="Destination Address",
        comodel_name="res.partner",
        related="move_id.partner_id",
        store=True,
    )