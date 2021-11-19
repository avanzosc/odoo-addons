# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.depends('product_id', 'account_id', 'partner_id', 'date',
                 'partner_id', 'move_id.analytic_account_id')
    def _compute_analytic_account_id(self):
        for record in self:
            if (not record.exclude_from_invoice_tab or not
                    record.move_id.is_invoice(include_receipts=True)):
                if (record.move_id.move_type not in
                    ('out_invoice', 'out_refund', 'out_receipt') or not
                        record.move_id.analytic_account_id):
                    super(AccountMoveLine, self)._compute_analytic_account_id()
                else:
                    record.analytic_account_id = (
                        record.move_id.analytic_account_id.id)

    def put_analytic_account_from_contact_type(self):
        cond = [
            ('exclude_from_invoice_tab', '=', False),
            ('move_id.move_type', 'not in',
             ('out_invoice', 'out_refund', 'out_receipt'))]
        lines = self.search(cond)
        for line in lines:
            partner = line.move_id.partner_id
            if partner.contact_type_id and not line.move_id.contact_type_id:
                line.move_id.contact_type_id = partner.contact_type_id.id
            if partner.contact_type_id.analytic_account_id:
                line.analytic_account_id = (
                    partner.contact_type_id.analytic_account_id.id)
