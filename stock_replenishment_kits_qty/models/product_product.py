import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    qty_in_kits = fields.Float(
        string="Quantity in Kits",
        compute="_compute_qty_in_kits",
        store=True,
        help="Total quantity of this product included in kits.",
    )

    def _compute_qty_in_kits(self):
        bom_line_obj = self.env["mrp.bom.line"]
        sale_line_obj = self.env["sale.order.line"]

        for product in self:
            try:
                bom_lines = bom_line_obj.search(
                    [
                        ("product_id", "=", product.id),
                        ("bom_id.type", "=", "phantom"),
                        ("bom_id.active", "=", True),
                    ]
                )
                total_qty = 0.0

                if bom_lines:
                    parent_product_ids = bom_lines.mapped(
                        "bom_id.product_tmpl_id.product_variant_ids"
                    )

                    sale_lines = sale_line_obj.search(
                        [
                            ("product_id", "in", parent_product_ids.ids),
                            ("state", "not in", ["sale", "done"]),
                        ]
                    )

                    for sale_line in sale_lines:
                        bom_line = bom_lines.filtered(
                            lambda line: line.bom_id.product_tmpl_id
                            == sale_line.product_id.product_tmpl_id
                        )
                        if bom_line:
                            total_qty += (
                                sale_line.product_uom_qty * bom_line.product_qty
                            )

                product.qty_in_kits = total_qty

            except Exception as e:
                _logger.error(
                    "Error computing qty in kits for product %s: %s", product.name, e
                )

    def button_calculate_qty_in_kits(self):
        self._compute_qty_in_kits()
