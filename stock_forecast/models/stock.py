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

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None,
                   orderby=False, lazy=True):
        if (self.env.context.get('to_date_expected', False) and
                self.env.context.get('my_operator', False)):
            domain.append(('date_expected_without_hour',
                           self.env.context.get('my_operator'),
                           self.env.context.get('to_date_expected')))
            if self.env.context.get('my_operator') != '<=':
                domain[0] = ('state', '=', 'done')
        return super(StockMove, self).read_group(
            domain, fields, groupby, offset=offset, limit=limit,
            orderby=orderby, lazy=lazy)
