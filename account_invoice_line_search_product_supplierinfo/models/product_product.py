# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        result = super().name_search(
            name=name, args=args, operator=operator, limit=limit
        )
        return self._put_normal_description(result)

    def _put_normal_description(self, result):
        for i, (pid, desc) in enumerate(result):
            product = self.env["product.product"].browse(pid)
            if product.default_code:
                name = ("[%(code)s] %(name)s") % {
                    "code": product.default_code,
                    "name": product.name,
                }
            else:
                name = product.name
            if desc != name:
                result[i] = (pid, name)
        return result
