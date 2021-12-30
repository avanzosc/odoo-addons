# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'

    picking_id = fields.Many2one(
        string='Transfer', comodel_name='stock.picking')
