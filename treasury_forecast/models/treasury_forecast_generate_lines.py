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
        active_model = self.env.context.get("active_model")
        active_ids = self.env.context.get("active_ids", [])
        if not active_ids:
            return {"type": "ir.actions.act_window_close"}
        if active_model == "treasury.financing":
            self._generate_from_financing(active_ids)
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

    def _generate_from_financing(self, active_ids):
        financing_model = self.env["treasury.financing"]
        financings = financing_model.browse(active_ids).exists()
        today = fields.Date.context_today(self)
        for financing in financings:
            recurrence = financing.installment_recurrence or 1
            recurrence = max(recurrence, 1)
            start_date = fields.Date.to_date(financing.start_date)
            anchor_day = start_date.day

            if financing.last_forecast_date:
                next_date = fields.Date.to_date(
                    financing.last_forecast_date
                ) + relativedelta(
                    months=recurrence,
                    day=anchor_day,
                )
            else:
                if start_date <= today:
                    next_date = today + relativedelta(day=anchor_day)
                else:
                    next_date = start_date
            while next_date <= self.date_limit:
                if financing.base_installment and financing.base_installment > 0:
                    self._create_financing_forecast_line(
                        financing,
                        next_date,
                        financing.base_installment,
                        financing.base_product_id,
                    )

                if (
                    financing.interest_installment
                    and financing.interest_installment > 0
                ):
                    self._create_financing_forecast_line(
                        financing,
                        next_date,
                        financing.interest_installment,
                        financing.interest_product_id,
                    )

                next_date = fields.Date.to_date(next_date) + relativedelta(
                    months=recurrence,
                    day=anchor_day,
                )

    def _create_financing_forecast_line(
        self, financing, line_date, amount, product_tmpl
    ):
        product = product_tmpl.product_variant_id if product_tmpl else False
        account = False
        if product:
            if financing.category_type == "income":
                account = product.property_account_income_id
            else:
                account = product.property_account_expense_id

        vals = {
            "date": line_date,
            "partner_id": financing.partner_id.id if financing.partner_id else False,
            "product_id": product.id if product else False,
            "name": financing.display_name,
            "journal_id": financing.journal_id.id if financing.journal_id else False,
            "recurrence_months": financing.installment_recurrence or 1,
            "active": True,
            "financing_id": financing.id,
            "category_id": financing.category_id.id if financing.category_id else False,
            "company_id": financing.company_id.id,
            "currency_id": financing.company_id.currency_id.id,
            "account_id": account.id if account else False,
        }
        if financing.category_type == "income":
            vals["income"] = amount
            vals["expense"] = 0.0
        else:
            vals["expense"] = amount
            vals["income"] = 0.0
        self.env["treasury.forecast"].create(vals)
