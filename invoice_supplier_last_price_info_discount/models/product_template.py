# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    last_supplier_move_discount = fields.Float(
        string="Last Supplier Move Discount (%)",
        digits="Discount",
        default=0.0,
        copy=False,
    )
    last_supplier_move_net_unit_price = fields.Float(default=0.0, copy=False)
