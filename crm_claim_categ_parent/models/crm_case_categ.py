# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class CrmCaseCateg(models.Model):
    _inherit = 'crm.case.categ'

    parent_id = fields.Many2one(
        comodel_name='crm.case.categ', string='Parent category', select=True)
