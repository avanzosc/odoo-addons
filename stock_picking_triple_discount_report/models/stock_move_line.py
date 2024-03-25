# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    sale_discount2 = fields.Float(
        related="sale_line.discount2", readonly=True, string="Sale discount 2(%)"
    )
    sale_discount3 = fields.Float(
        related="sale_line.discount3", readonly=True, string="Sale discount 3(%)"
    )
