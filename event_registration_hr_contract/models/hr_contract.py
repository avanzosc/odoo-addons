# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class HrContract(models.Model):
    _inherit = 'hr.contract'

    registrations = fields.One2many(
        comodel_name='event.registration', string='Registrations',
        inverse_name='contract')
