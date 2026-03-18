from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class TreasuryFinancing(models.Model):
    _name = "treasury.financing"
    _description = "Financing"

    code = fields.Char(required=True)
    name = fields.Char(required=True)
    partner_id = fields.Many2one(
        "res.partner",
    )
    journal_id = fields.Many2one("account.journal", domain=[("type", "=", "bank")])

    display_name = fields.Char(
        compute="_compute_display_name",
        store=True,
    )

    category_type = fields.Selection(
        selection=[
            ("income", "Income"),
            ("expense", "Expense"),
        ],
        string="Type",
        related="category_id.category_type",
        store=True,
        readonly=True,
    )

    contract_date = fields.Date()
    start_date = fields.Date(string="Installment Start Date")
    end_date = fields.Date(string="Installment End Date")

    installment_recurrence = fields.Integer(
        string="Installment Recurrence (Months)", default=1
    )

    interest_review_recurrence = fields.Integer(
        string="Interest Review Recurrence (Months)",
        default=6,
    )

    installment_number = fields.Integer(string="Number of Installments")

    interest_conditions = fields.Text(string="condicions interest")

    total_amount = fields.Float(string="amount total")

    base_installment = fields.Float(string="installment base")

    current_interest_percent = fields.Float(string="Current Interest (%)")

    interest_installment = fields.Float(string="installment interest")

    installment_amount = fields.Float(
        string="amount installment",
        compute="_compute_installment_amount",
        store=True,
    )

    category_id = fields.Many2one(
        "treasury.financing.category",
        string="Categoría",
        required=True,
    )
    parent_category_id = fields.Many2one(
        "treasury.financing.category",
        string="Parent Category",
        related="category_id.parent_id",
        store=True,
        readonly=True,
    )

    base_product_id = fields.Many2one(
        "product.template",
        string="Product base",
        domain=[("type", "=", "service")],
    )

    interest_product_id = fields.Many2one(
        "product.template",
        string="Product interest",
        domain=[("type", "=", "service")],
    )

    last_forecast_date = fields.Date(
        string="forecast last date",
        compute="_compute_last_forecast_date",
    )

    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.company,
    )

    forecast_line_count = fields.Integer(
        string="Forecast Lines",
        compute="_compute_forecast_line_count",
    )

    def _compute_forecast_line_count(self):
        for record in self:
            if record.id:
                forecast_lines = self.env["treasury.forecast"].search_count(
                    [("financing_id", "=", record.id)]
                )
                record.forecast_line_count = forecast_lines
            else:
                record.forecast_line_count = 0

    def action_view_forecast_lines(self):
        self.ensure_one()
        forecast_lines = self.env["treasury.forecast"].search(
            [("financing_id", "=", self.id)]
        )
        action = self.env["ir.actions.actions"]._for_xml_id(
            "treasury_forecast.action_treasury_forecast"
        )
        if len(forecast_lines) > 1:
            action["domain"] = [("id", "in", forecast_lines.ids)]
        elif len(forecast_lines) == 1:
            action["views"] = [
                (
                    self.env.ref("treasury_forecast.view_treasury_forecast_form").id,
                    "form",
                )
            ]
            action["res_id"] = forecast_lines.id
        return action

    @api.depends("code", "name")
    def _compute_display_name(self):
        for rec in self:
            if rec.code and rec.name:
                rec.display_name = f"{rec.code} {rec.name}"
            else:
                rec.display_name = rec.code or rec.name or ""

    @api.depends("base_installment", "interest_installment")
    def _compute_installment_amount(self):
        for rec in self:
            rec.installment_amount = (rec.base_installment or 0.0) + (
                rec.interest_installment or 0.0
            )

    def _compute_last_forecast_date(self):
        forecast_model = self.env["treasury.forecast"]
        for rec in self:
            last_forecast = forecast_model.search(
                [("financing_id", "=", rec.id)],
                order="date desc, id desc",
                limit=1,
            )
            rec.last_forecast_date = last_forecast.date if last_forecast else False

    def action_open_generate_lines_wizard(self):
        if len(self) > 1:
            wizard_model = self.env["treasury.forecast.generate.lines"]
            for record in self:
                wizard = wizard_model.create(
                    {
                        "date_limit": record.end_date,
                    }
                )
                wizard = wizard.with_context(
                    active_ids=[record.id],
                    active_model="treasury.financing",
                )
                wizard.action_generate()

            return {"type": "ir.actions.act_window_close"}

        self.ensure_one()

        if not self.start_date:
            raise ValidationError(_("Debe indicar la fecha inicio cuotas."))

        today = fields.Date.context_today(self)
        start_date = fields.Date.to_date(self.start_date)

        if self.last_forecast_date:
            base_date = self.last_forecast_date
        else:
            if self.start_date <= today:
                base_date = today + relativedelta(day=start_date.day)
            else:
                base_date = self.start_date

        wizard_date = fields.Date.to_date(base_date) + relativedelta(
            months=self.interest_review_recurrence or 0
        )
        if self.end_date and wizard_date > fields.Date.to_date(self.end_date):
            wizard_date = fields.Date.to_date(self.end_date)

        action = self.env.ref(
            "treasury_forecast.action_treasury_forecast_generate_lines"
        ).read()[0]

        action["context"] = dict(
            self.env.context,
            active_ids=self.ids,
            active_model="treasury.financing",
            default_date_limit=self.end_date,
        )
        return action
