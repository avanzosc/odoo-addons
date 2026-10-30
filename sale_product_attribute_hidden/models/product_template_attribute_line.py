# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class ProductTemplateAttributeLine(models.Model):
    _inherit = "product.template.attribute.line"

    def _is_hidden_in_configuration(self):
        self.ensure_one()
        return (
            self.attribute_id.hide_in_configuration
            and self.attribute_id.create_variant == "no_variant"
        )

    def _is_configurable(self):
        return not self._is_hidden_in_configuration() and super()._is_configurable()
