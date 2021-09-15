# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrderHistory(models.Model):
    _name = "sale.order.history"
    _description = "Sale Order History"

    name = fields.Char(string="Description", required=True)
    partner = fields.Char(string="Partner")
    partner_id = fields.Many2one("res.partner", string="Partner")
    amount_tax = fields.Float(string="Taxes", default=0.0)
    amount_total = fields.Float(string="Total", default=0.0)
    amount_untaxed = fields.Float(string="Amount untaxed", default=0.0)
    confirmation_date = fields.Date(string="Confirmation Date")
    order_date = fields.Date(string="Order Date")
    history_line_ids = fields.One2many(
        comodel_name="sale.order.line.history", inverse_name="order_id",
        string="Order History Lines")


class SaleOrderLineHistory(models.Model):
    _name = "sale.order.line.history"
    _description = "Sale Order Line History"

    order_id = fields.Many2one(
        comodel_name="sale.order.history", string="Order Reference",
        required=True, readonly=True)
    partner_id = fields.Many2one(
        relation="sale.order.history", string="Partner", readonly=True,
        related="order_id.partner_id")
    partner = fields.Char(string="Partner", readonly=True,
                          related="order_id.partner")
    name = fields.Text(string="Description", required=True)
    price_unit = fields.Float("Unit Price", readonly=True, default=0.0)
    discount = fields.Float(string="Discount (%)", readonly=True, default=0.0)
    product = fields.Char(string="Product", readonly=True)
    product_uom_qty = fields.Float(string="Ordered Quantity", default=1.0,
                                   readonly=True)
    product_uos_qty = fields.Float(string="Ordered Quantity (UoS)",
                                   default=1.0, readonly=True)
    product_uom = fields.Char(string="Unit of Measure", readonly=True)
    type = fields.Char(string="Type", readonly=True)
    salesman = fields.Char(string="Salesperson", readonly=True)
    invoiced = fields.Boolean(string="Invoiced", default=True, readonly=True)
