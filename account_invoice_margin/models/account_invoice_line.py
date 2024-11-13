from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.move.line"

    product_cost = fields.Float(
        string="Product Cost",
        related="product_id.standard_price",
        store=True,
    )
    subtotal_cost = fields.Float(
        string="Subtotal Cost",
        compute="_compute_subtotal_cost",
        store=True,
    )
    margin = fields.Float(
        string="Margin",
        compute="_compute_margin",
        store=True,
    )
    margin_percent = fields.Float(
        string="Margin Percent",
        compute="_compute_margin_percent",
        store=True,
    )

    @api.depends("product_cost", "quantity")
    def _compute_subtotal_cost(self):
        for line in self:
            line.subtotal_cost = line.product_cost * line.quantity

    @api.depends("subtotal_cost", "price_subtotal")
    def _compute_margin(self):
        for line in self:
            line.margin = line.price_subtotal - line.subtotal_cost

    @api.depends("margin", "price_subtotal")
    def _compute_margin_percent(self):
        for line in self:
            if line.price_subtotal != 0:
                line.margin_percent = (line.margin / line.price_subtotal) * 100
            else:
                line.margin_percent = 0
