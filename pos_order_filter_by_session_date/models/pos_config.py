# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from datetime import datetime, time

from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    def read_config_open_orders(self, domain, record_ids=None):
        if record_ids is None:
            record_ids = {}

        open_session = self.env["pos.session"].search(
            [
                ("config_id", "=", self.id),
                ("state", "in", ["opening_control", "opened"]),
            ],
            limit=1,
        )

        if open_session and open_session.start_at:
            session_date = open_session.start_at.date()
        else:
            session_date = fields.Date.today()

        day_start = fields.Datetime.to_string(datetime.combine(session_date, time.min))

        if "pos.order" in domain:
            domain["pos.order"] = [("date_order", ">=", day_start)] + list(
                domain["pos.order"]
            )

        if record_ids.get("pos.order"):
            record_ids = dict(record_ids)
            record_ids["pos.order"] = (
                self.env["pos.order"]
                .search(
                    [
                        ("id", "in", record_ids["pos.order"]),
                        ("date_order", ">=", day_start),
                    ]
                )
                .ids
            )

        return super().read_config_open_orders(domain, record_ids)
