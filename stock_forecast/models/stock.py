# -*- coding: utf-8 -*-
# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.multi
    @api.depends('date_expected')
    def _compute_date_expected_without_hour(self):
        for move in self:
            move.date_expected_without_hour = (
                fields.Datetime.from_string(move.date_expected).date() if
                move.date_expected else False)

    date_expected_without_hour = fields.Date(
        strint='Date expected without hour',
        compute='_compute_date_expected_without_hour', store=True)


class Stockquant(models.Model):
    _inherit = "stock.quant"

    @api.multi
    @api.depends('in_date')
    def _compute_in_date_without_hour(self):
        for quant in self:
            quant.in_date_without_hour = (
                fields.Datetime.from_string(quant.in_date).date() if
                quant.in_date else False)

    in_date_without_hour = fields.Date(
        strint='In date without hour', compute='_compute_in_date_without_hour',
        store=True)

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None,
                   context=None, orderby=False, lazy=True):
        if self.env.context.get('to_date_expected', False):
            domain.append(('in_date_without_hour', '<',
                           self.env.context.get('to_date_expected')))
        return super(Stockquant, self).read_group(
            domain, fields, groupby, offset=offset, limit=limit,
            context=context, orderby=orderby, lazy=lazy)
