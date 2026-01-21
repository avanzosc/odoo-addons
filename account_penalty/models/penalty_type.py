# Copyright 2025 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PenaltyType(models.Model):
    _name = "penalty.type"
    _description = "Penalty Type"

    name = fields.Char(required=True)
    product_id = fields.Many2one("product.product", required=True)
