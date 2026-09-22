# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductRma(models.TransientModel):
    _name = "product.rma"
    _description = "Products in RMAs"
    _order = "sale_line_id, product_rma"

    sale_line_id = fields.Many2one(
        string="Sale line",
        comodel_name="sale.order.line",
        copy=False,
    )
    product_rma = fields.Text(
        string="Product",
        copy=False,
    )
    product_uom_id = fields.Many2one(
        string="UoM",
        comodel_name="uom.uom",
        copy=False,
    )
    quantity = fields.Float(
        digits="Product Unit of Measure",
        copy=False,
    )
    amount = fields.Monetary(
        copy=False,
        currency_field="currency_id",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        copy=False,
    )
