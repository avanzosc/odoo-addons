# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    acc_balance = fields.Float(string="Balance", related="account_id.balance")


class AccountMove(models.Model):

    _inherit = 'account.move'

    @api.multi
    def button_cancel(self):
        acc_move_line_obj = self.env['account.move.line']
        for move in self:
            acc_move_line_obj._update_journal_check(move.journal_id.id,
                                                    move.period_id.id)
        return super(AccountMove, self).button_cancel()
