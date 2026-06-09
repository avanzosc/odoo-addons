# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    generic_repair_product = fields.Boolean(
        string="Generic Repair Product",
        default=False,
        help="It's a generic repair product?",
    )

    @api.constrains("generic_repair_product")
    def _check_generic_repair_product(self):
        for template in self.filtered(lambda x: x.generic_repair_product):
            cond = [("id", "!=", template.id), ("generic_repair_product", "=", True)]
            other_template = self.env["product.template"].search(cond, limit=1)
            if other_template:
                error = _(
                    "The product: %(product)s it is already marked as "
                    "generic repair product."
                ) % {"product": other_template.name}
                raise ValidationError(error)
