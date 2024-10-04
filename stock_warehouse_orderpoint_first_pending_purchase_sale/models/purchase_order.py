# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import pytz

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    date_planned_without_hour = fields.Date(
        copy=False, store=True, compute="_compute_date_planned_without_hour"
    )

    @api.depends("date_planned")
    def _compute_date_planned_without_hour(self):
        for purchase in self:
            date_planned_without_hour = False
            if purchase.date_planned:
                local_dt = purchase.date_planned.astimezone(
                    pytz.timezone(self.env.user.tz or "UTC")
                )
                date_planned_without_hour = local_dt.date()
            self.date_planned_without_hour = date_planned_without_hour
