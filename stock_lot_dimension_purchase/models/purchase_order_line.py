# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models

from odoo.addons.stock_lot_dimension.models.product_category import (
    PRICING_METHOD_SELECTION,
)


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    product_length = fields.Float(string="Length", digits="Product Dimension")
    product_weight = fields.Float(string="Weight", digits="Product Dimension Weight")
    purchase_weight = fields.Float(
        string="Weight/Unit",
        digits="Product Dimension Weight",
        readonly=True,
    )
    purchase_weight_uom_id = fields.Many2one(comodel_name="uom.uom", readonly=True)
    purchase_length = fields.Float(
        string="Length/Unit",
        digits="Product Dimension",
        readonly=True,
    )
    purchase_length_uom_id = fields.Many2one(comodel_name="uom.uom", readonly=True)
    pricing_method = fields.Selection(
        selection=PRICING_METHOD_SELECTION,
        default="qty",
    )
    dimension_qty = fields.Float(
        string="Dim. Qty",
        digits="Product Dimension",
        compute="_compute_dimension_qty",
        store=True,
        readonly=False,
    )

    @api.depends(
        "pricing_method",
        "product_weight",
        "product_length",
    )
    def _compute_dimension_qty(self):
        for line in self:
            dimension_qty = 1.0

            if line.pricing_method == "weight":
                dimension_qty = line.product_weight

            elif line.pricing_method == "length":
                dimension_qty = line.product_length

            elif line.pricing_method == "wl":
                dimension_qty = line.product_weight * line.product_length

            line.dimension_qty = dimension_qty

    @api.onchange("product_id")
    def onchange_product_id(self):
        res = super().onchange_product_id()
        product = self.product_id

        self.purchase_weight = 0.0
        self.purchase_weight_uom_id = False
        self.purchase_length = 0.0
        self.purchase_length_uom_id = False

        if product:
            self.pricing_method = product.pricing_method
            self.product_length = product.product_length
            self.purchase_length_uom_id = product.dimensional_uom_id.id
            self.product_weight = product.weight
            self.purchase_weight_uom_id = self.env[
                "product.template"
            ]._get_weight_uom_id_from_ir_config_parameter()

            if self.order_id.partner_id:
                seller = product._select_seller(
                    partner_id=self.order_id.partner_id,
                    quantity=self.product_qty,
                    date=(
                        self.order_id.date_order.date()
                        if self.order_id.date_order
                        else fields.Date.context_today(self)
                    ),
                    uom_id=self.product_uom,
                    params=self._get_select_sellers_params(),
                )

                if seller:
                    self.purchase_weight = seller.purchase_weight
                    self.purchase_weight_uom_id = seller.purchase_weight_uom_id.id
                    self.purchase_length = seller.purchase_length
                    self.purchase_length_uom_id = seller.purchase_length_uom_id.id
                    if seller.purchase_weight:
                        self.product_weight = seller.purchase_weight
                    if seller.purchase_length:
                        self.product_length = seller.purchase_length
        else:
            self.pricing_method = "qty"
            self.product_length = 0.0
            self.product_weight = 0.0

        return res

    @api.depends(
        "product_qty",
        "price_unit",
        "taxes_id",
        "discount",
        "dimension_qty",
        "pricing_method",
    )
    def _compute_amount(self):
        return super()._compute_amount()

    def _prepare_base_line_for_taxes_computation(self):
        self.ensure_one()
        base_line = super()._prepare_base_line_for_taxes_computation()
        if self.pricing_method in ("weight", "length", "wl"):
            base_line["quantity"] = self.product_qty * self.dimension_qty
        return base_line

    def _prepare_account_move_line(self, move=False):
        self.ensure_one()
        res = super()._prepare_account_move_line(move=move)
        if self.pricing_method in ("weight", "length", "wl"):
            res["price_unit"] *= self.dimension_qty
        return res
