# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models
from odoo.tools import float_round


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    product_packaging_id = fields.Many2one(compute=False, precompute=False)
    product_packaging_qty = fields.Float(
        compute=False, precompute=False, string="Pack. Quantity"
    )

    @api.onchange("product_packaging_id")
    def _onchange_product_packaging_id(self):
        if self.product_packaging_id:
            self.product_packaging_qty = 1
            self.product_uom_qty = self.product_packaging_id.qty
        else:
            self.product_packaging_qty = 0
            self.product_uom_qty = 1

    @api.onchange("product_qty")
    def _onchange_product_qty(self):
        if self.product_packaging_id and self.product_uom_qty:
            packaging_uom = self.product_packaging_id.product_uom_id
            packaging_uom_qty = self.product_uom._compute_quantity(
                self.product_uom_qty, packaging_uom
            )
            self.product_packaging_qty = float_round(
                packaging_uom_qty / self.product_packaging_id.qty,
                precision_rounding=packaging_uom.rounding,
            )

    @api.onchange("product_id")
    def onchange_product_id(self):
        result = super().onchange_product_id()
        if self.product_id and self.product_id.packaging_ids:
            packagings = self.product_id.packaging_ids.filtered(lambda x: x.purchase)
            if packagings:
                self.product_packaging_id = packagings[0].id
        return result
