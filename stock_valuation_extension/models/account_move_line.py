# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    stock_move_id = fields.Many2one(comodel_name='stock.move',
                                    string='Stock Move')
