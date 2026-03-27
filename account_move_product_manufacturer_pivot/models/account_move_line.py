from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

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

    @api.depends("product_id")
    def _compute_pivot_manufacturer_id(self):
        for line in self:
            production_id = self.env["mrp.production"].search(
                [("product_id", "=", line.product_id.id)], limit=1
            )
            if production_id:
                line.pivot_manufacturer_id = (
                    production_id.manufacturer_id.id
                    if production_id.manufacturer_id
                    else False
                )
            else:
                line.pivot_manufacturer_id = False
