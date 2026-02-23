# Copyright 2026 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from dateutil.relativedelta import relativedelta

from odoo import fields, models


class TreasuryForecastGenerateLines(models.TransientModel):
    _name = "treasury.forecast.generate.lines"
    _description = "Generate Treasury Lines"

    date_limit = fields.Date(required=True, default=fields.Date.context_today)

    def action_generate(self):
        self.ensure_one()
        active_ids = self.env.context.get("active_ids", [])
        if not active_ids:
            return {"type": "ir.actions.act_window_close"}

        line_model = self.env["treasury.forecast"].with_context(active_test=False)
        selected_lines = line_model.browse(active_ids).exists()
        processed_keys = set()
        for line in selected_lines:
            key = (line.partner_id.id or False, line.product_id.id)
            if key in processed_keys:
                continue
            processed_keys.add(key)
            domain = [("product_id", "=", key[1])]
            if key[0]:
                domain.append(("partner_id", "=", key[0]))
            else:
                domain.append(("partner_id", "=", False))

            latest_line = line_model.search(domain, order="date desc, id desc", limit=1)
            if not latest_line or not latest_line.date:
                continue

            recurrence = latest_line.recurrence_months or 1
            recurrence = max(recurrence, 1)
            next_date = fields.Date.to_date(latest_line.date) + relativedelta(
                months=recurrence
            )
            while next_date <= self.date_limit:
                latest_line = latest_line.copy(default={"date": next_date})
                next_date = fields.Date.to_date(latest_line.date) + relativedelta(
                    months=recurrence
                )

        return {"type": "ir.actions.act_window_close"}
