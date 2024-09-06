# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    name_for_labels = fields.Char(
        string="Name for labels", compute="_compute_name_for_labels"
    )

    def _compute_name_for_labels(self):
        max_length = int(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("product_name_max_length_for_labels", default=55)
        )
        for product in self:
            name_for_labels = ""
            if max_length > len(product.name):
                name_for_labels = product.name
            else:
                name_for_labels = product.name[0:max_length]
            product.name_for_labels = name_for_labels
