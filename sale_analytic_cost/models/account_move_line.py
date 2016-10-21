# -*- coding: utf-8 -*-
# (c) 2015 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, api


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    @api.model
    def _prepare_analytic_line(self, obj_line):
        res = super(AccountMoveLine, self)._prepare_analytic_line(obj_line)
        if obj_line.journal_id.type == 'sale' and obj_line.product_id:
            res['estim_std_cost'] = (-obj_line.quantity *
                                     obj_line.product_id.manual_standard_cost)
            res['estim_avg_cost'] = (-obj_line.quantity *
                                     obj_line.product_id.standard_price)
        return res
