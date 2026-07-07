from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    origin_not_exists = fields.Boolean(
        string="Missing Origin",
        compute="_compute_origin_not_exists",
        store=True,
    )

    def _resolve_origin_name(self, picking, visited=None):
        if visited is None:
            visited = set()
        if not picking or not picking.origin or picking.id in visited:
            return None

        visited.add(picking.id)

        origin_parts = picking.origin.strip().split()
        first_word = origin_parts[0]

        if first_word in ("Return", "Retorno") and len(origin_parts) >= 2:
            referenced_name = origin_parts[-1]
            referenced_picking = self.env["stock.picking"].search(
                [
                    ("name", "=", referenced_name),
                    ("company_id", "=", picking.company_id.id),
                ],
                limit=1,
            )
            return self._resolve_origin_name(referenced_picking, visited)
        else:
            return first_word

    @api.depends("origin")
    def _compute_origin_not_exists(self):
        SaleOrder = self.env["sale.order"]
        PurchaseOrder = self.env["purchase.order"]

        for picking in self:
            category = picking.picking_type_id.category_id.name
            if (
                not picking.origin
                or picking.state != "done"
                or category not in ("Compra", "Venta")
            ):
                picking.origin_not_exists = False
                continue

            origin_name = self._resolve_origin_name(picking)
            company_id = picking.company_id.id

            if not origin_name:
                picking.origin_not_exists = False
                continue

            has_sale = (
                SaleOrder.search_count(
                    [("name", "=", origin_name), ("company_id", "=", company_id)]
                )
                > 0
            )

            has_purchase = (
                PurchaseOrder.search_count(
                    [
                        "|",
                        ("name", "=", origin_name),
                        ("partner_ref", "=", origin_name),
                        ("company_id", "=", company_id),
                    ]
                )
                > 0
            )

            has_order = (
                self.env["stock.move"].search_count(
                    [
                        ("picking_id", "=", picking.id),
                        "|",
                        ("sale_line_id", "!=", False),
                        ("purchase_line_id", "!=", False),
                        ("company_id", "=", company_id),
                    ]
                )
                > 0
            )

            picking.origin_not_exists = not (has_sale or has_purchase) and not has_order
