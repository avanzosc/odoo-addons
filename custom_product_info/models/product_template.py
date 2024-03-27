# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    diameter = fields.Integer(
        string="Diameter"
    )
    hardness = fields.Integer(
        string="Hardness"
    )
    core_color_id = fields.Many2one(
        string="Core Color",
        comodel_name="product.color"
    )
    wheel_color_id = fields.Many2one(
        string="Wheel Color",
        comodel_name="product.color"
    )
