# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class AccountTax(models.Model):
    _inherit = 'account.tax'

    invoice_printing_note = fields.Text(
        string='Invoice printing note', translate=True)


class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    invoice_printing_note = fields.Text(
        string='Invoice printing note', translate=True)
