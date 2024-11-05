from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    basket_lines = fields.One2many(
        comodel_name="mrp.bom.line",
        inverse_name="product_tmpl_id",
        compute="_compute_basket_lines",
        store=True,
    )
    count_component_kit = fields.Integer(
        compute="_compute_count_component_kit",
        store=True,
    )

    @api.depends("bom_ids", "bom_ids.bom_line_ids.product_id")
    def _compute_basket_lines(self):
        for product in self:
            bom_lines = self.env["mrp.bom.line"].search(
                [
                    ("product_id", "=", product.id),
                    ("bom_id.is_basket", "=", True),
                    ("bom_id.type", "=", "phantom"),
                    ("bom_id.active", "=", True),
                    ("active", "=", True),
                ]
            )
            product.basket_lines = bom_lines

    @api.depends("basket_lines")
    def _compute_count_component_kit(self):
        for product in self:
            product.count_component_kit = len(product.basket_lines)
