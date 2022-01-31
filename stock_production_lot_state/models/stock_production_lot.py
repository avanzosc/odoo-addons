# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    state = fields.Selection(
        [('new', 'New'),
         ('active', 'Active'),
         ('inactive', 'Inactive'),
         ('finished', 'Finished')],
        string="State",
        default='new',
        copy=False)
