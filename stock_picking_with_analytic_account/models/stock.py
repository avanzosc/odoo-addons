# -*- coding: utf-8 -*-
# Copyright (c) 2017 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account', string='Analytic account',
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]})

    @api.onchange('analytic_account_id')
    def onchange_analytic_account_id(self):
        for picking in self.filtered(lambda x: x.analytic_account_id and
                                     x.analytic_account_id.partner_id):
            picking.partner_id = picking.analytic_account_id.partner_id.id


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _action_done(self):
        moves = super(StockMove, self)._action_done()
        for move in moves.filtered(
            lambda x: x.picking_id and
            x.picking_id.analytic_account_id and
                x.picking_id.picking_type_code in ('outgoing', 'incoming')):
            vals = move._prepare_data_for_create_analytic_line()
            self.env['account.analytic.line'].create(vals)

    def _prepare_data_for_create_analytic_line(self):
        vals = {'account_id': self.picking_id.analytic_account_id.id,
                'partner_id': self.picking_id.partner_id.id,
                'product_id': self.product_id.id,
                'product_uom_id': self.product_uom.id,
                'unit_amount': self.product_qty,
                'amount': self.product_qty * self.price_unit,
                'name': u"{} {}".format(self.picking_id.name, self.name)}
        return vals
