from odoo import api, fields, models


class MRPBomLine(models.Model):
    _inherit = "mrp.bom.line"

    is_basket = fields.Boolean(
        compute="_compute_is_basket",
        store=True,
    )

    @api.depends("bom_id.product_tmpl_id.is_basket")
    def _compute_is_basket(self):
        for line in self:
            line.is_basket = line.bom_id.product_tmpl_id.is_basket
