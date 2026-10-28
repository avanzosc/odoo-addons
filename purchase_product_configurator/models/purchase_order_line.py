from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    configurator_product_tmpl_id = fields.Many2one(
        comodel_name="product.template",
        related="product_id.product_tmpl_id",
        readonly=True,
    )
    is_configurable_product = fields.Boolean(
        related="product_id.product_tmpl_id.has_configurable_attributes",
        readonly=True,
    )
    configurator_pricelist_id = fields.Many2one(
        comodel_name="product.pricelist",
        compute="_compute_configurator_pricelist_id",
        compute_sudo=True,
    )
    configurator_currency_id = fields.Many2one(
        comodel_name="res.currency",
        related="order_id.currency_id",
        readonly=True,
    )

    @api.depends("company_id")
    def _compute_configurator_pricelist_id(self):
        """Supply the pricelist argument required by sale's standard dialog RPC.

        The dialog itself is the standard Sale ProductConfiguratorDialog.
        The final purchase line price is still recomputed by purchase.order.line
        after the configured product/quantity are applied.
        """
        Pricelist = self.env["product.pricelist"]
        for line in self:
            line.configurator_pricelist_id = Pricelist.search(
                [
                    "|",
                    ("company_id", "=", False),
                    ("company_id", "=", line.company_id.id),
                ],
                order="company_id desc, id",
                limit=1,
            )
