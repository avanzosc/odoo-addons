# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    repair_id = fields.One2many(
        comodel_name='mrp.repair', inverse_name='invoice_id',
        string='Repair Order')
