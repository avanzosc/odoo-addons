# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, api


class StockQuant(models.Model):

    _inherit = 'stock.quant'

    @api.model
    def _prepare_account_move_line(self, move, qty, cost, credit_account_id,
                                   debit_account_id):
        res = super(StockQuant, self)._prepare_account_move_line(
            move, qty, cost, credit_account_id, debit_account_id)
        for record in res:
            record[2]['stock_move_id'] = move.id
        return res


class StockMove(models.Model):

    _inherit = 'stock.move'

    @api.multi
    def product_price_update_production_done(self):
        aml_obj = self.env['account.move.line']
        res = super(StockMove, self).product_price_update_production_done()
        for move in self.filtered(
                lambda x: (x.production_id and
                           x.product_id.cost_method == 'real' and
                           x.product_id.valuation == 'real_time')):
            amount = sum(move.mapped('quant_ids.inventory_value'))
            credit_acc = (
                move.product_id.property_stock_account_input or
                move.product_id.categ_id.property_stock_account_input_categ)
            aml_credit = aml_obj.search([('stock_move_id', '=', move.id),
                                         ('account_id', '=', credit_acc.id)],
                                        limit=1)
            aml_debit = aml_credit.move_id.line_id.filtered(lambda x: x.id !=
                                                            aml_credit.id)
            aml_debit.write({'debit': len(aml_debit) and
                             (amount / len(aml_debit)) or 0})
            aml_credit.write({'credit': amount})
        return res
