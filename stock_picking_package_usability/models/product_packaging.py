# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    packaging_length = fields.Float(string="Pack Length")
    width = fields.Float(string="Pack Width")
    height = fields.Float(string="Pack Height")
    packaging_length_bck = fields.Float()
    width_bck = fields.Float()
    height_bck = fields.Float()
    empty_weight = fields.Float(
        string="weight empty",
    )

    def _auto_init(self):
        result = super()._auto_init()
        self.env.cr.execute(
            """
            UPDATE product_packaging
               SET packaging_length = COALESCE(
                       packaging_length_bck, packaging_length
                   ),
                   width = COALESCE(width_bck, width),
                   height = COALESCE(height_bck, height)
            """
        )
        self.env.cr.execute(
            """
            UPDATE product_packaging
               SET packaging_length_bck = COALESCE(
                       packaging_length_bck, packaging_length
                   ),
                   width_bck = COALESCE(width_bck, width),
                   height_bck = COALESCE(height_bck, height)
            """
        )
        return result

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._set_dimension_bck(vals)
        return super().create(vals_list)

    def write(self, vals):
        vals = dict(vals)
        self._set_dimension_bck(vals)
        return super().write(vals)

    @api.model
    def _set_dimension_bck(self, vals):
        field_mapping = {
            "packaging_length": "packaging_length_bck",
            "width": "width_bck",
            "height": "height_bck",
        }
        for field_name, bck_field_name in field_mapping.items():
            if vals.get(field_name):
                vals[bck_field_name] = vals[field_name]
