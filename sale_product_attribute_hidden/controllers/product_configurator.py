# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.addons.sale.controllers import product_configurator


class HiddenAttributeProductConfiguratorMixin:
    def _get_product_information(self, product_template, combination, *args, **kwargs):
        hidden_lines = product_template.attribute_line_ids.filtered(
            lambda line: line._is_hidden_in_configuration()
        )
        combination = combination.filtered(
            lambda value: value.attribute_line_id not in hidden_lines
        )
        values = super()._get_product_information(
            product_template, combination, *args, **kwargs
        )
        values["attribute_lines"] = [
            line
            for line in values["attribute_lines"]
            if line["id"] not in hidden_lines.ids
        ]
        return values


class SaleProductConfiguratorController(
    HiddenAttributeProductConfiguratorMixin,
    product_configurator.SaleProductConfiguratorController,
):
    pass
