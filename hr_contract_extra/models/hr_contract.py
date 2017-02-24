# -*- coding: utf-8 -*-
# © 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


from openerp import fields, models


class HrContract(models.Model):
    _inherit = 'hr.contract'

    compensation_ids = fields.One2many(
        comodel_name='hr.contract.compensation', string='Compensation',
        inverse_name='contract_id')
