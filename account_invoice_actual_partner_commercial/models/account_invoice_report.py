
from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    current_user_id = fields.Many2one(
        comodel_name='res.users', related='partner_id.user_id',
        string="Current customer salesperson", store=True)
