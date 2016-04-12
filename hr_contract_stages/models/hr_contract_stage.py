# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class HrContractStage(models.Model):
    _name = 'hr.contract.stage'
    _order = 'sequence'

    name = fields.Char()
    sequence = fields.Integer(string='Sequence',
                              help='Used to order stages. Lower is better.')
