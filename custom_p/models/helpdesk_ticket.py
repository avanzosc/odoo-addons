# Copyright 2025 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    name = fields.Char(tracking=True)
    last_message_date = fields.Datetime(
        compute="_compute_last_message_date", store=True
    )

    @api.depends("message_ids", "message_ids.date")
    def _compute_last_message_date(self):
        for ticket in self:
            date = False
            if ticket.message_ids:
                date = max(ticket.message_ids, key=lambda x: x.date).date
            ticket.last_message_date = date
