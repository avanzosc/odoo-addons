from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.move"

    total_product_cost = fields.Float(
        string="Total Product Cost",
        compute="_compute_total_product_cost",
        store=True,
    )
    total_margin = fields.Float(
        string="Total Margin",
        compute="_compute_total_margin",
        store=True,
    )
    average_margin_percent = fields.Float(
        string="Average Margin Percent",
        compute="_compute_average_margin_percent",
        store=True,
    )

    @api.depends("invoice_line_ids.subtotal_cost")
    def _compute_total_product_cost(self):
        for invoice in self:
            invoice.total_subtotal_cost = sum(
                invoice.invoice_line_ids.mapped("product_cost")
            )

    @api.depends("invoice_line_ids.margin")
    def _compute_total_margin(self):
        for invoice in self:
            invoice.total_margin = sum(invoice.invoice_line_ids.mapped("margin"))

    @api.depends("invoice_line_ids.margin_percent")
    def _compute_average_margin_percent(self):
        for invoice in self:
            margin_percent_values = invoice.invoice_line_ids.mapped("margin_percent")
            if margin_percent_values:
                invoice.average_margin_percent = sum(margin_percent_values) / len(
                    margin_percent_values
                )
            else:
                invoice.average_margin_percent = 0
