# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    product_categ_id = fields.Many2one(
        "product.category",
        string="Product Category",
        related="product_id.categ_id",
        store=True,
        readonly=True,
    )
