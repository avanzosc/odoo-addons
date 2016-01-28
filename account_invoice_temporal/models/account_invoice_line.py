# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    temporal = fields.Boolean(related='account_id.temporal')
