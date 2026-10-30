# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.addons.sale.controllers import combo_configurator


class HiddenAttributeComboConfiguratorMixin:
    def _get_ptals_data(self, product, *args, **kwargs):
        hidden_lines = product.attribute_line_ids.filtered(
            lambda line: line._is_hidden_in_configuration()
        )
        return [
            line
            for line in super()._get_ptals_data(product, *args, **kwargs)
            if line["id"] not in hidden_lines.ids
        ]


class SaleComboConfiguratorController(
    HiddenAttributeComboConfiguratorMixin,
    combo_configurator.SaleComboConfiguratorController,
):
    pass
