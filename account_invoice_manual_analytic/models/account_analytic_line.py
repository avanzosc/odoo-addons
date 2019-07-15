# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    from_invoice_id = fields.Many2one(
        comodel_name='account.invoice', ondelete="cascade",
        string='Generated manually from invoice')
