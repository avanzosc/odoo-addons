# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import pytz

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    date_deadline_without_hour = fields.Date(
        compute="_compute_date_deadline_without_hour",
        store=True,
        copy=False,
    )

    @api.depends("date_deadline")
    def _compute_date_deadline_without_hour(self):
        for move in self:
            date_deadline_without_hour = False
            if move.date_deadline:
                local_dt = move.date_deadline.astimezone(
                    pytz.timezone(self.env.user.tz or "UTC")
                )
                date_deadline_without_hour = local_dt.date()
            self.date_deadline_without_hour = date_deadline_without_hour
