# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    cmr_tractor_id = fields.Many2one(domain="[('category', '=', 'head')]")
    cmr_semi_trailer_id = fields.Many2one(domain="[('category', '=', 'trailer')]")
