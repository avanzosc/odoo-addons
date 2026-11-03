import re

from odoo import api, models
from odoo.osv import expression


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        if not self._context.get("from_purchase"):
            return super()._name_search(
                name,
                args=args,
                operator=operator,
                limit=limit,
                name_get_uid=name_get_uid,
            )
        if not args:
            args = []
        if name:
            positive_operators = ["=", "ilike", "=ilike", "like", "=like"]
            product_ids = []

            if self._context.get("partner_id"):
                suppliers_ids = self.env["product.supplierinfo"]._search(
                    [
                        ("partner_id", "=", self._context.get("partner_id")),
                        "|",
                        ("product_code", operator, name),
                        ("product_name", operator, name),
                    ],
                    access_rights_uid=name_get_uid,
                )
                if suppliers_ids:
                    product_ids = list(
                        self._search(
                            [("product_tmpl_id.seller_ids", "in", suppliers_ids)]
                            + args,
                            limit=limit,
                            access_rights_uid=name_get_uid,
                        )
                    )

            if not product_ids and operator in positive_operators:
                product_ids = list(
                    self._search(
                        [("default_code", "=", name)] + args,
                        limit=limit,
                        access_rights_uid=name_get_uid,
                    )
                )

                if not product_ids:
                    product_ids = list(
                        self._search(
                            [("barcode", "=", name)] + args,
                            limit=limit,
                            access_rights_uid=name_get_uid,
                        )
                    )

            if not product_ids and operator not in expression.NEGATIVE_TERM_OPERATORS:
                products_query = self._search(
                    args + [("default_code", operator, name)], limit=limit
                )
                product_ids = list(products_query)
                if not limit or len(product_ids) < limit:
                    limit2 = (limit - len(product_ids)) if limit else False
                    product2_ids = self._search(
                        args
                        + [("name", operator, name), ("id", "not in", products_query)],
                        limit=limit2,
                        access_rights_uid=name_get_uid,
                    )
                    product_ids.extend(product2_ids)
            elif not product_ids and operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = expression.OR(
                    [
                        [
                            "&",
                            ("default_code", operator, name),
                            ("name", operator, name),
                        ],
                        ["&", ("default_code", "=", False), ("name", operator, name)],
                    ]
                )
                domain = expression.AND([args, domain])
                product_ids = list(
                    self._search(domain, limit=limit, access_rights_uid=name_get_uid)
                )

            if not product_ids and operator in positive_operators:
                ptrn = re.compile(r"(\[(.*?)\])")
                res = ptrn.search(name)
                if res:
                    product_ids = list(
                        self._search(
                            [("default_code", "=", res.group(2))] + args,
                            limit=limit,
                            access_rights_uid=name_get_uid,
                        )
                    )
        else:
            product_ids = list(
                self._search(args, limit=limit, access_rights_uid=name_get_uid)
            )
        return product_ids
