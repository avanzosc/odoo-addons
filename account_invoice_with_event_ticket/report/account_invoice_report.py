# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    event_id = fields.Many2one(
        string='Event', comodel_name='event.event', readonly=True)
    event_ticket_id = fields.Many2one(
        string='Event ticket', comodel_name='event.event.ticket',
        readonly=True)
    event_address_id = fields.Many2one(
        string='Event address', comodel_name='res.partner', readonly=True)

    @api.model
    def _select(self):
        return super(AccountInvoiceReport, self)._select() + \
            ", line.event_id, line.event_ticket_id, line.event_address_id"
