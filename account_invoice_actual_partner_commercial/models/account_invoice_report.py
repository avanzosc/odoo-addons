
from odoo import api, fields, models


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    current_user_id = fields.Many2one(
        comodel_name='res.users',
        string='Current customer salesperson',
        #compute='_compute_invoice_current_user',
        readonly=True)

    @api.depends('partner_id', 'partner_id.user_id')
    def _compute_invoice_current_user(self):
        for record in self:
            record.current_user_id = record.partner_id.user_id.id

    def _select(self):
        return super(AccountInvoiceReport, self)._select() + \
            ", sub.current_user_id as current_user_id"

    def _sub_select(self):
        return super(AccountInvoiceReport, self)._sub_select() + \
            ", ai.current_user_id as current_user_id"

    def _group_by(self):
        return super(AccountInvoiceReport, self)._group_by() + \
            ", ai.current_user_id"

