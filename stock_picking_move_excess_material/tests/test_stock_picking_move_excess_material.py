# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests.common import TransactionCase


class TestStockPickingMoveExcessMaterial(TransactionCase):

    def setUp(self):
        super(TestStockPickingMoveExcessMaterial, self).setUp()
        partner_obj = self.env['res.partner']
        picking_obj = self.env['stock.picking']
        quant_obj = self.env['stock.quant']
        cond = [('reserved_quantity', '>', 0)]
        quant = quant_obj.search(cond, limit=1)
        self.product = quant.product_id
        self.product_qty_available = quant.quantity
        self.product_quant_reserved_quantity = quant.reserved_quantity
        cond = [('supplier', '=', True)]
        self.supplier = partner_obj.search(cond, limit=1)
        cond = [('code', '=', 'incoming')]
        self.in_picking_type = self.env['stock.picking.type'].search(
            cond, limit=1)
        picking_vals = {
            'partner_id': self.supplier.id,
            'picking_type_id': self.in_picking_type.id,
            'location_id': quant.location_id.id,
            'location_dest_id': quant.location_id.id}
        self.picking = picking_obj.create(picking_vals)

    def test_stock_picking_move_excess_material(self):
        self.picking.action_move_excess_material()
        line = self.picking.move_lines.filtered(
            lambda x: x.product_id == self.product)
        dif = self.product_qty_available - self.product_quant_reserved_quantity
        self.assertEquals(line.product_uom_qty, dif)
