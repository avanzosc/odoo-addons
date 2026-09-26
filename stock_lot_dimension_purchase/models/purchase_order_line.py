# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.model
    def _get_dimension_uom_domain(self):
        return [("category_id", "=", self.env.ref("uom.uom_categ_length").id)]

    product_length = fields.Float(string="Length", digits="Product Unit of Measure")
    product_height = fields.Float(string="Height", digits="Product Unit of Measure")
    product_width = fields.Float(string="Width", digits="Product Unit of Measure")
    dimensional_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="Dimensional UoM",
        domain=lambda self: self._get_dimension_uom_domain(),
        help="UoM for length, height, width",
        default=lambda self: self.env.ref("uom.product_uom_meter"),
    )
    volume = fields.Float(
        compute="_compute_volume",
        readonly=False,
        store=True,
    )
    product_weight = fields.Float(string="Weight", digits="Stock Weight")
    purchase_weight = fields.Float(string="Weight/Unit", readonly=True)
    purchase_weight_uom_id = fields.Many2one(comodel_name="uom.uom", readonly=True)
    purchase_length = fields.Float(string="Length/Unit", readonly=True)
    purchase_length_uom_id = fields.Many2one(comodel_name="uom.uom", readonly=True)
    pricing_method = fields.Selection(
        selection=[
            ("qty", "Quantity"),
            ("weight", "Weight"),
            ("length", "Length"),
            ("wl", "Weight*Length"),
        ],
    )
    dimension_qty = fields.Float(string="Dim. Qty")

    @api.depends(
        "product_length", "product_height", "product_width", "dimensional_uom_id"
    )
    def _compute_volume(self):
        template_obj = self.env["product.template"]
        for lot in self:
            lot.volume = template_obj._calc_volume(
                lot.product_length,
                lot.product_height,
                lot.product_width,
                lot.dimensional_uom_id,
            )

    @api.onchange(
        "pricing_method",
        "dimension_qty",
        "purchase_weight",
        "purchase_length",
    )
    def onchange_pricing_method(self):
        if self.pricing_method and self.pricing_method == "weight":
            qty = self.purchase_weight_uom_id._compute_quantity(
                self.purchase_weight,
                self.product_uom,
            )
            self.product_qty = self.dimension_qty * qty
        elif self.pricing_method and self.pricing_method == "length":
            qty = self.purchase_length_uom_id._compute_quantity(
                self.purchase_length,
                self.product_uom,
            )
            self.product_qty = self.dimension_qty * qty
        elif self.pricing_method and self.pricing_method == "wl":
            self.product_qty = (
                self.dimension_qty
                * self.product_height
                * self.purchase_length
                * self.purchase_weight
            )

    @api.onchange("product_id")
    def onchange_product_id(self):
        product = self.product_id
        if product:
            self.pricing_method = product.pricing_method
            self.product_length = product.product_length
            self.product_height = product.product_height
            self.product_width = product.product_width
            self.dimensional_uom_id = product.dimensional_uom_id.id
            self.product_weight = product.weight
        return super().onchange_product_id()

    @api.onchange("product_id", "partner_id")
    def onchange_product_supplierinfo(self):
        product_supplierinfo = (
            self.product_id._select_seller(
                partner_id=self.partner_id,
                quantity=self.product_qty,
                date=self.order_id.date_order
                and self.order_id.date_order.date()
                or fields.Date.context_today(self),
                uom_id=self.product_uom,
                params=self._get_select_sellers_params(),
            )
            if self.product_id
            else False
        )
        if product_supplierinfo:
            self.purchase_weight = product_supplierinfo.purchase_weight
            self.purchase_weight_uom_id = product_supplierinfo.purchase_weight_uom_id.id
            self.purchase_length = product_supplierinfo.purchase_length
            self.purchase_length_uom_id = product_supplierinfo.purchase_length_uom_id.id
            self.dimension_qty = product_supplierinfo.min_qty
