# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    responsible_id = fields.Many2one(
        string='Responsible', comodel_name='res.partner')
