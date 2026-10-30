# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    hide_in_configuration = fields.Boolean(
        string="Hide in product configuration",
        help="The attribute is not used in the variant grid of sales and "
        "purchases nor in the product configurator, and it is not shown on the "
        "product page of the online shop. Products can still be filtered by it. "
        "Only for attributes that never create variants.",
    )

    @api.constrains("hide_in_configuration", "create_variant")
    def _check_hide_in_configuration(self):
        for attribute in self:
            if (
                attribute.hide_in_configuration
                and attribute.create_variant != "no_variant"
            ):
                raise ValidationError(
                    _(
                        "Attribute %(attribute)s creates variants, so it cannot "
                        "be hidden in the product configuration.",
                        attribute=attribute.display_name,
                    )
                )
