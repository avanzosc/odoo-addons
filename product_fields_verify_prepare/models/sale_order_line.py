from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    verification_by = fields.Selection(
        related="product_id.product_tmpl_id.verification_by",
        string="Verification by",
        readonly=True,
    )

    preparation = fields.Selection(
        related="product_id.product_tmpl_id.preparation",
        string="Preparation",
        readonly=True,
    )

    def _prepare_procurement_group_vals(self):
        res = super()._prepare_procurement_group_vals()
        if self.product_id.type == "service":
            res.update(
                {
                    "verification_by": self.verification_by,
                    "preparation": self.preparation,
                }
            )
        return res
