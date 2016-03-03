# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import _, api, exceptions, models


class AccountInvoiceConfirm(models.TransientModel):
    _inherit = "account.invoice.confirm"

    @api.multi
    def invoice_confirm(self):
        active_ids = self.env.context.get('active_ids', []) or []
        invoice_obj = self.env['account.invoice']
        for account in invoice_obj.browse(active_ids):
            if account.state not in ('draft', 'proforma', 'proforma2'):
                raise exceptions.Warning(_(
                    "Selected invoice(s) cannot be confirmed as they are not"
                    " in 'Draft' or 'Pro-Forma' state."))
            account.check_temporal()
            account.signal_workflow('invoice_open')
        return {'type': 'ir.actions.act_window_close'}
