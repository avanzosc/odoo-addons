# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class ContractContact(models.Model):
    _inherit = 'contract.contract'

    def _prepare_invoice(self, date_invoice, journal=None):
        fiscal_position_obj = self.env['account.fiscal.position']
        invoice_vals, move_form = super(
            ContractContact, self)._prepare_invoice(
                date_invoice, journal=journal)
        if ('partner_id' in invoice_vals and
            invoice_vals.get('partner_id', False) and
            'contact_type_id' in invoice_vals and
            invoice_vals.get('contact_type_id', False) and
            'analytic_account_id' in invoice_vals and
                invoice_vals.get('analytic_account_id', False)):
            invoice_vals['analytic_account_id'] = False
        if ('fiscal_position_id' in invoice_vals and
                invoice_vals.get('fiscal_position_id', False)):
            fiscal_position = fiscal_position_obj.sudo().browse(
                invoice_vals.get('fiscal_position_id'))
            if (fiscal_position.company_id.id !=
                    invoice_vals.get('company_id', False)):
                invoice_vals['fiscal_position_id'] = False
        return invoice_vals, move_form
