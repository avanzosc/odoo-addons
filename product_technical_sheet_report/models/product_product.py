# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models

PLY_ATTRIBUTE_NAMES = ("Top", "M2", "M3", "M4", "M5", "M6", "Bottom")


class ProductProduct(models.Model):
    _inherit = "product.product"

    @staticmethod
    def _format_technical_sheet_measure(value):
        return f"{value:.2f}".rstrip("0").rstrip(".")

    def get_technical_sheet_attribute_value(self, attribute_name):
        self.ensure_one()
        values = self.product_template_attribute_value_ids.product_attribute_value_id
        return values.filtered(
            lambda value: value.attribute_id.name.strip().casefold()
            == attribute_name.strip().casefold()
        )[:1]

    def get_technical_sheet_shape(self):
        self.ensure_one()
        return self.get_technical_sheet_attribute_value("SHAPE").shape_id

    def get_technical_sheet_plies(self):
        self.ensure_one()
        return [
            (attribute_name, self.get_technical_sheet_attribute_value(attribute_name))
            for attribute_name in PLY_ATTRIBUTE_NAMES
            if self.get_technical_sheet_attribute_value(attribute_name)
        ]

    def get_technical_sheet_size(self):
        self.ensure_one()
        shape = self.get_technical_sheet_shape()
        if not shape or not shape.sale_width:
            return ""
        return f'{shape.sale_width:g}"'

    def get_technical_sheet_dimensions_mm(self):
        self.ensure_one()
        shape = self.get_technical_sheet_shape()
        if not shape or not shape.width_mm or not shape.length_mm:
            return ""
        width = self._format_technical_sheet_measure(shape.width_mm)
        length = self._format_technical_sheet_measure(shape.length_mm)
        return f"{width} x {length} mm"

    def get_technical_sheet_dimensions_in(self):
        self.ensure_one()
        shape = self.get_technical_sheet_shape()
        if not shape or not shape.width_in or not shape.length_in:
            return ""
        width = self._format_technical_sheet_measure(shape.width_in)
        length = self._format_technical_sheet_measure(shape.length_in)
        return f'{width}" x {length}"'

    def get_technical_sheet_wheelbase(self, field_name):
        self.ensure_one()
        shape = self.get_technical_sheet_shape()
        value = shape[field_name] if shape else 0.0
        if not value:
            return ""
        return f'{self._format_technical_sheet_measure(value)}"'

    def get_technical_sheet_season(self):
        self.ensure_one()
        return self.seasonality_ids[:1].display_name or ""
