# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    palet_id = fields.Many2one(
        string="Palet", comodel_name="stock.package.type", copy=False)
    palet_qty = fields.Float(
        string="Palet Quantity", default=1,
        digits="Product Unit of Measure", copy=False)

    @api.onchange("product_packaging_id")
    def _onchange_product_packaging_id(self):
        result = super(
            PurchaseOrderLine, self)._onchange_product_packaging_id()
        if self.product_packaging_id and self.product_packaging_id.palet_id.id:
            self.palet_id = self.product_packaging_id.palet_id.id
        else:
            self.palet_id = False
            self.palet_qty = 0
        if self.palet_id and self.product_uom_qty:
            self.palet_qty = self._get_palet_qty()
        return result

    @api.onchange("product_qty")
    def _onchange_product_qty(self):
        result = super(PurchaseOrderLine, self)._onchange_product_qty()
        if self.palet_id and self.product_uom_qty:
            self.palet_qty = self._get_palet_qty()
        return result

    def _get_palet_qty(self):
        return (self.product_uom_qty /
                (self.product_packaging_id.qty *
                 self.product_packaging_id.palet_qty))
