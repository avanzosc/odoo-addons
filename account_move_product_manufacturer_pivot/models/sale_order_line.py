from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_category_id = fields.Many2one(
        related="product_id.categ_id",
        string="Product Category",
        store=True,
    )

    pivot_manufacturer_id = fields.Many2one(
        "hr.employee",
        string="Pivot Manufacturer",
        compute="_compute_pivot_manufacturer_id",
        store=True,
    )

    manufacturer_id = fields.Many2one(
        "product.manufacturer",
        string="Manufacturer",
        related="product_id.manufacturer_id",
        store=True,
    )

    @api.depends("order_id.production_ids")
    def _compute_pivot_manufacturer_id(self):
        for line in self:
            production_id = line.order_id.production_ids.filtered(
                lambda p: p.product_id == line.product_id
            )[:1]
            if production_id:
                line.pivot_manufacturer_id = production_id.manufacturer_id.id or False
            else:
                line.pivot_manufacturer_id = False
