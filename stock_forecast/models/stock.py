# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    date_expected_without_hour = fields.Date(
        string='Date expected without hour',
        compute='_compute_date_expected_without_hour', store=True)

    @api.depends('date_expected')
    def _compute_date_expected_without_hour(self):
        for move in self:
            move.date_expected_without_hour = (
                move.date_expected.date() if move.date_expected else False)
