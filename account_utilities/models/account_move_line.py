# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    acc_balance = fields.Float(string="Balance", related="account_id.balance")
