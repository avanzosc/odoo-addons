# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    activity_type_id = fields.Many2one(
        comodel_name="mail.activity.type", string="Activity type",
        compute="_compute_activity_info", store=True, copy=False
        )
    activity_date = fields.Date(
        string="Activity date", compute="_compute_activity_info", store=True,
        copy=False
        )
    activity_user_id = fields.Many2one(
        comodel_name="res.users", string="Activity user",
        compute="_compute_activity_info", store=True, copy=False
        )

    @api.multi
    @api.depends("activity_ids", "activity_ids.activity_type_id",
                 "activity_ids.date_deadline", "activity_ids.user_id")
    def _compute_activity_info(self):
        for invoice in self:
            lines = False
            activity_type = False
            activity_date = False
            activity_user = False
            if invoice.activity_ids:
                lines = min(
                    invoice.activity_ids, key=lambda x: x.date_deadline)
                if lines and len(lines) > 1:
                    lines = min(lines, key=lambda x: x.create_date)
            if lines and lines.activity_type_id:
                activity_type = lines.activity_type_id.id
            if lines and lines.date_deadline:
                activity_date = lines.date_deadline
            if lines and lines.user_id:
                activity_user = lines.user_id.id
            invoice.activity_type_id = activity_type
            invoice.activity_date = activity_date
            invoice.activity_user_id = activity_user
