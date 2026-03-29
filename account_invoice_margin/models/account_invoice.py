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
    total_margin_percent = fields.Float(
        string="Total Margin Percent",
        compute="_compute_margin_percent",
        store=True,
    )

    @api.depends("invoice_line_ids.subtotal_cost")
    def _compute_total_product_cost(self):
        for invoice in self:
            invoice.total_product_cost = sum(
                invoice.invoice_line_ids.mapped("product_cost")
            )

    @api.depends("invoice_line_ids.subtotal_cost", "invoice_line_ids.price_total")
    def _compute_total_margin(self):
        for invoice in self:
            total_cost = sum(invoice.invoice_line_ids.mapped("product_cost"))
            total_sales = sum(invoice.invoice_line_ids.mapped("price_total"))
            invoice.total_margin = total_sales - total_cost

    @api.depends("total_margin", "invoice_line_ids.price_total")
    def _compute_margin_percent(self):
        for invoice in self:
            total_sales = sum(invoice.invoice_line_ids.mapped("price_total"))
            if total_sales != 0:
                invoice.total_margin_percent = (
                    invoice.total_margin / total_sales
                ) * 100
            else:
                invoice.total_margin_percent = 0
