# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class AccountInvoiceSend(models.TransientModel):
    _inherit = "account.invoice.send"

    notify_followers = fields.Boolean(default=True)

    @api.multi
    def send_mail(self, auto_commit=False):
        ctx = self.env.context.copy()
        for wizard in self:
            if wizard.composer_id:
                wizard.composer_id.notify_followers = wizard.notify_followers
            ctx['notify_followers'] = wizard.notify_followers
            wizard = wizard.with_context(ctx)
            super(AccountInvoiceSend, wizard).send_mail(
                auto_commit=auto_commit)
        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def send_and_print_action(self):
        self.ensure_one()
        ctx = self.env.context.copy()
        ctx['notify_followers'] = self.notify_followers
        self.composer_id.notify_followers = self.notify_followers
        wizard = self.with_context(ctx)
        return super(AccountInvoiceSend, wizard).send_and_print_action()
