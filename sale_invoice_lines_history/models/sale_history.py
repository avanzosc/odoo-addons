# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# Copyright (c) 2026 Eñaut Alberdi - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrderHistory(models.Model):
    _name = "sale.order.history"
    _description = "Sale Order History"

    name = fields.Char(string="Description", required=True)
    partner = fields.Char()
    partner_id = fields.Many2one("res.partner")
    amount_tax = fields.Float(string="Taxes", default=0.0)
    amount_total = fields.Float(string="Total", default=0.0)
    amount_untaxed = fields.Float(string="Amount untaxed", default=0.0)
    confirmation_date = fields.Date()
    order_date = fields.Date()
    history_lines = fields.One2many(
        comodel_name="sale.order.line.history",
        inverse_name="order_id",
        string="Order History Lines",
    )


class SaleOrderLineHistory(models.Model):
    _name = "sale.order.line.history"
    _description = "Sale Order Line History"

    order_id = fields.Many2one(
        comodel_name="sale.order.history", string="Order Reference", required=True
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner", related="order_id.partner_id", readonly=False
    )
    partner = fields.Char(compute="_compute_partner", store=True, readonly=False)
    name = fields.Text(string="Description", required=True)
    price_unit = fields.Float("Unit Price", default=0.0)
    discount = fields.Float(string="Discount (%)", default=0.0)
    product = fields.Char()
    product_uom_qty = fields.Float(string="Ordered Quantity", default=1.0)
    product_uos_qty = fields.Float(string="Ordered Quantity (UoS)", default=1.0)
    product_uom = fields.Char(string="Unit of Measure")
    type = fields.Char()
    salesman = fields.Char(string="Salesperson")
    invoiced = fields.Boolean(default=True)

    @api.depends("order_id.partner", "order_id.partner_id.name")
    def _compute_partner(self):
        for line in self:
            line.partner = (
                line.order_id.partner or line.order_id.partner_id.name or False
            )
