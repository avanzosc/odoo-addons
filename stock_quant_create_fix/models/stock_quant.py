# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import inspect

from odoo import models
from odoo.osv import expression


class StockQuant(models.Model):
    _inherit = "stock.quant"

    def _gather(
        self,
        product_id,
        location_id,
        lot_id=None,
        package_id=None,
        owner_id=None,
        strict=False,
        qty=0,
        **kwargs,
    ):
        quants_cache = self.env.context.get("quants_cache")
        removal_strategy = self._get_removal_strategy(product_id, location_id)
        if quants_cache is not None and strict and removal_strategy != "least_packages":
            quants = self.env["stock.quant"]
            lot_ids = [False]
            if lot_id:
                lot_ids.insert(0, lot_id.id)
            package_ids = [False] if not package_id else [package_id.id, False]
            owner_ids = [False] if not owner_id else [owner_id.id, False]
            for lot_cache_id in lot_ids:
                for package_cache_id in package_ids:
                    for owner_cache_id in owner_ids:
                        quants |= quants_cache[
                            product_id.id,
                            location_id.id,
                            lot_cache_id,
                            package_cache_id,
                            owner_cache_id,
                        ]
            if removal_strategy == "closest":
                quants = quants.sorted(lambda q: (q.location_id.complete_name, -q.id))
            return quants.sorted(lambda q: not q.lot_id)
        super_gather = super()._gather
        gather_kwargs = {
            "lot_id": lot_id,
            "package_id": package_id,
            "owner_id": owner_id,
            "strict": strict,
            **kwargs,
        }
        super_params = inspect.signature(super_gather).parameters
        if "qty" in super_params or any(
            p.kind == inspect.Parameter.VAR_KEYWORD for p in super_params.values()
        ):
            gather_kwargs["qty"] = qty
        return super_gather(product_id, location_id, **gather_kwargs)

    def _get_gather_domain(
        self,
        product_id,
        location_id,
        lot_id=None,
        package_id=None,
        owner_id=None,
        strict=False,
    ):
        domain = [("product_id", "=", product_id.id)]
        if not strict:
            if lot_id:
                domain = expression.AND(
                    [["|", ("lot_id", "=", lot_id.id), ("lot_id", "=", False)], domain]
                )
            if package_id:
                domain = expression.AND(
                    [
                        [
                            "|",
                            ("package_id", "=", package_id.id),
                            ("package_id", "=", False),
                        ],
                        domain,
                    ]
                )
            if owner_id:
                domain = expression.AND(
                    [
                        ["|", ("owner_id", "=", owner_id.id), ("owner_id", "=", False)],
                        domain,
                    ]
                )
            domain = expression.AND(
                [[("location_id", "child_of", location_id.id)], domain]
            )
        else:
            domain = expression.AND(
                [
                    ["|", ("lot_id", "=", lot_id.id), ("lot_id", "=", False)]
                    if lot_id
                    else [("lot_id", "=", False)],
                    domain,
                ]
            )
            domain = expression.AND(
                [
                    [
                        "|",
                        ("package_id", "=", package_id.id),
                        ("package_id", "=", False),
                    ]
                    if package_id
                    else [("package_id", "=", False)],
                    domain,
                ]
            )
            domain = expression.AND(
                [
                    ["|", ("owner_id", "=", owner_id.id), ("owner_id", "=", False)]
                    if owner_id
                    else [("owner_id", "=", False)],
                    domain,
                ]
            )
            domain = expression.AND([[("location_id", "=", location_id.id)], domain])
        if self.env.context.get("with_expiration"):
            domain = expression.AND(
                [
                    [
                        "|",
                        ("expiration_date", ">=", self.env.context["with_expiration"]),
                        ("expiration_date", "=", False),
                    ],
                    domain,
                ]
            )
        return domain
