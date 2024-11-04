from odoo import api, fields, models


class MRPBom(models.Model):
    _inherit = "mrp.bom"

    is_basket = fields.Boolean(
        compute="_compute_is_basket",
        store=True,
    )

    @api.depends("product_tmpl_id.is_basket")
    def _compute_is_basket(self):
        for bom in self:
            bom.is_basket = bom.product_tmpl_id.is_basket
