from odoo import models, fields

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    internal_notes = fields.Text(string="Internal Notes", tracking=True)
