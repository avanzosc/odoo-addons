# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockPackageType(models.Model):
    _inherit = "stock.package.type"

    qty_per_layer = fields.Integer(
        string="Quantity per Layer",
        default=1,
        help="Number of packages of this type that fit in a single layer "
        "when stacked on a pallet. Used to estimate the height of a "
        "pallet from the number of inner packages it contains.",
    )

    @api.constrains("base_weight", "height", "width", "packaging_length")
    def _check_positive_dimensions(self):
        for package_type in self:
            if package_type.base_weight <= 0:
                raise ValidationError(
                    _(
                        "The empty weight of package type '%s' must be "
                        "greater than zero."
                    )
                    % package_type.name
                )
            if package_type.height <= 0:
                raise ValidationError(
                    _("The height of package type '%s' must be greater " "than zero.")
                    % package_type.name
                )
            if package_type.width <= 0:
                raise ValidationError(
                    _("The width of package type '%s' must be greater " "than zero.")
                    % package_type.name
                )
            if package_type.packaging_length <= 0:
                raise ValidationError(
                    _("The length of package type '%s' must be greater " "than zero.")
                    % package_type.name
                )
