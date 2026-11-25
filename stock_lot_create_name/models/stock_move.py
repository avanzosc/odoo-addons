# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models
from odoo.tools.float_utils import float_compare


class StockMove(models.Model):
    _inherit = "stock.move"

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        self.ensure_one()
        vals = super()._prepare_move_line_vals(
            quantity=quantity, reserved_quant=reserved_quant
        )
        picking_id = vals.get("picking_id")
        product_id = vals.get("product_id")
        quantity = vals.get("quantity")
        uom_id = vals.get("product_uom_id")
        if not (picking_id and product_id and quantity and uom_id):
            return vals
        picking = self.env["stock.picking"].browse(picking_id)
        picking_type = picking.picking_type_id
        if not (picking_type.use_create_lots and picking_type.lot_code):
            return vals
        product = self.env["product.product"].browse(product_id)
        if product.tracking != "lot":
            return vals
        uom = self.env["uom.uom"].browse(uom_id)
        if not float_compare(quantity, 0, precision_rounding=uom.rounding):
            return vals
        vals["lot_name"] = f"{picking.picking_type_id.lot_code}{picking.name[4:]}"
        return vals
