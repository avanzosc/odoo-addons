# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = "product.product"

    generic_repair_product = fields.Boolean(
        string="Generic Repair Product",
        related="product_tmpl_id.generic_repair_product",
        store=True,
    )

    @api.constrains("generic_repair_product")
    def _check_generic_repair_product(self):
        for product in self.filtered(lambda x: x.generic_repair_product):
            cond = [("id", "!=", product.id), ("generic_repair_product", "=", True)]
            other_product = self.env["product.product"].search(cond, limit=1)
            if other_product:
                error = _(
                    "The product variant: %(product)s it is already marked as "
                    "generic repair product."
                ) % {"product": other_product.name}
                raise ValidationError(error)
