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

    @api.depends(
        "bom_ids.bom_line_ids",
        "bom_ids.bom_line_ids.product_tmpl_id",
        "bom_ids.bom_line_ids.is_basket",
        "bom_ids.type",
        "bom_ids.active",
        "bom_ids.product_tmpl_id.active",
    )
    def _compute_basket_lines(self):
        for product in self:
            product.basket_lines = self.env["mrp.bom.line"].search(
                [
                    ("product_tmpl_id", "=", product.id),
                    ("is_basket", "=", True),
                    ("bom_id.type", "=", "phantom"),
                    ("bom_id.active", "=", True),
                    ("bom_id.product_tmpl_id.active", "=", True),
                ]
            )
            product.count_component_kit = len(product.basket_lines)

    @api.depends("basket_lines")
    def _compute_count_component_kit(self):
        for product in self:
            product.count_component_kit = len(product.basket_lines)
