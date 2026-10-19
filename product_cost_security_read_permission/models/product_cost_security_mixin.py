# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class ProductCostSecurityMixin(models.AbstractModel):
    _inherit = "product.cost.security.mixin"

    @api.model
    def check_field_access_rights(self, operation, fields):
        if (
            self._name == "product.product"
            and operation == "read"
            and "standard_price" in fields
            and not self.env.user.has_group("product_cost_security.group_product_cost")
        ):
            return super(
                ProductCostSecurityMixin, self.sudo()
            ).check_field_access_rights(operation, fields)
        return super().check_field_access_rights(operation, fields)
