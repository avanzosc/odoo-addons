# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    lot_id = fields.Many2one(
        string='Mother',
        comodel_name='stock.production.lot')
