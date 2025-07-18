# Copyright 2025 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.tools import html_sanitize


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    name = fields.Char(tracking=True)
    last_message_date = fields.Datetime(
        compute="_compute_last_message_date", store=True
    )

    def write(self, vals):
        for record in self:
            if (
                vals.get("description")
                and html_sanitize(vals.get("description")) != record.description
            ):
                record.message_post(
                    body_is_html=True,
                    body=_("Description: %s --> %s")
                    % (record.description, vals.get("description")),
                )
        res = super().write(vals)
        return res

    @api.depends("message_ids", "message_ids.date")
    def _compute_last_message_date(self):
        for ticket in self:
            date = False
            if ticket.message_ids:
                date = max(ticket.message_ids, key=lambda x: x.date).date
            ticket.last_message_date = date
