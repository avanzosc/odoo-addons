# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    category_type_id = fields.Many2one(
        string="Product Section",
        comodel_name="category.type",
        related="product_id.category_type_id",
        store=True,
    )
