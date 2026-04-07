# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_old_reference = fields.Char(string="Old reference", index=True, copy=False)

    @api.model
    def _name_search(
        self, name="", args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        res = super()._name_search(
            name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid
        )
        res_ids = list(res)
        res_ids_len = len(res_ids)
        if not limit or res_ids_len >= limit:
            limit = (limit - res_ids_len) if limit else False
        if not name and limit or res_ids_len >= limit:
            return res_ids
        limit -= res_ids_len
        product_ids = list(
            self._search(
                [("product_old_reference", operator, name)],
                limit=limit,
                access_rights_uid=name_get_uid,
            )
        )
        res_ids.extend(product_ids)
        return res_ids
