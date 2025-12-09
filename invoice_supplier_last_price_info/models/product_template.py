# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    last_supplier_move_price = fields.Float(
        string="Last supplier move price",
        digits="Product Price",
    )
    last_supplier_move_date = fields.Date(
        string="Last supplier move date",
    )
    last_supplier_move_id = fields.Many2one(
        comodel_name="res.partner", string="Last supplier move"
    )
