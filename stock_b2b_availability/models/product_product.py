# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    b2b_virtual_available = fields.Float(
        string="B2B Quantity",
        compute="_compute_b2b_quantities",
        digits="Product Unit of Measure",
    )

    @api.depends(
        "stock_move_ids.product_qty", "stock_move_ids.state", "stock_move_ids.quantity"
    )
    @api.depends_context(
        "lot_id",
        "owner_id",
        "package_id",
        "from_date",
        "to_date",
        "location",
        "warehouse_id",
        "allowed_company_ids",
        "is_storable",
    )
    def _compute_b2b_quantities(self):
        locations = self.env["stock.location"].search([("for_stock_b2b", "=", True)])
        products = (
            self.with_context(prefetch_fields=False)
            .filtered(lambda p: p.type != "service")
            .with_context(prefetch_fields=True)
        )
        res = products.with_context(location=locations.ids)._compute_quantities_dict(
            self._context.get("lot_id"),
            self._context.get("owner_id"),
            self._context.get("package_id"),
            self._context.get("from_date"),
            self._context.get("to_date"),
        )
        # Set qty fields to 0 for all products as services have 0 quantities.
        # Also skips calling __setitem__ on products with 0 quantites in res.
        self.b2b_virtual_available = 0.0
        for product in products:
            product.update(
                {
                    "b2b_virtual_available": res[product.id]["virtual_available"],
                }
            )
