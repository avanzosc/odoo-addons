# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestStockProductionLotWithPartner(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.location_model = cls.env['stock.location']
        cls.partner_model = cls.env['res.partner']
        cls.line_model = cls.env['stock.move.line']
        cls.lot_model = cls.env['stock.production.lot']
        cls.picking_type_model = cls.env['stock.picking.type']
        cls.picking_model = cls.env['stock.picking']
        cond = [('supplier', '=', True)]
        cls.supplier = cls.partner_model.search(cond, limit=1)
        cond = [('customer', '=', True)]
        cls.customer = cls.partner_model.search(cond, limit=1)
        cls.product = cls.env['product.product'].search(
            [('type', '=', 'product')], limit=1)
        cls.product.write({'tracking': 'lot'})
        cond = [('code', '=', 'outgoing')]
        cls.out_picking_type = cls.picking_type_model.search(cond, limit=1)
        cls.location_customer = cls.location_model.search(
            [('usage', '=', 'customer')], limit=1)
        out_picking_vals = {
            'partner_id': cls.customer.id,
            'picking_type_id': cls.out_picking_type.id,
            'location_id': cls.out_picking_type.default_location_src_id.id,
            'location_dest_id': cls.location_customer.id}
        out_picking_line_vals = {
            'product_id': cls.product.id,
            'name': cls.product.name,
            'product_uom_qty': 5,
            'product_uom': cls.product.uom_id.id}
        out_picking_vals['move_lines'] = [(0, 0, out_picking_line_vals)]
        cls.out_picking = cls.picking_model.create(out_picking_vals)
        move_data = [(0, 0,
                      {'product_id': cls.product.id,
                       'product_uom_id': cls.product.uom_id.id,
                       'product_uom_qty': 5})]
        cls.out_picking.move_ids_without_package.write(
            {'move_ids_without_package': move_data})

    def test_lot_with_partner_in_picking(self):
        lot1_vals = {
            'name': 'TestStockProductionLotWithPartner lot 1',
            'product_id': self.product.id}
        lot1 = self.lot_model.create(lot1_vals)
        lot2_vals = {
            'name': 'TestStockProductionLotWithPartner lot 2',
            'product_id': self.product.id}
        lot2 = self.lot_model.create(lot2_vals)
        cond = [('state', '=', 'draft'),
                ('picking_type_id.code', '=', 'incoming')]
        picking = self.picking_model.search(cond, limit=1)
        line_vals = {
            'picking_id': picking.id,
            'product_id': self.product.id,
            'product_uom_id': self.product.uom_id.id,
            'location_id': picking.location_id.id,
            'location_dest_id': picking.location_dest_id.id,
            'lot_id': lot1.id}
        line = self.line_model.create(line_vals)
        self.assertEquals(line.lot_id.name,
                          'TestStockProductionLotWithPartner lot 1')
        self.assertEquals(line.lot_id.supplier_id.id, picking.partner_id.id)
        line.write({'lot_id': lot2.id})
        self.assertEquals(line.lot_id.name,
                          'TestStockProductionLotWithPartner lot 2')
        self.assertEquals(line.lot_id.supplier_id.id, picking.partner_id.id)

    def test_lot_with_partner_out_picking(self):
        self.assertEquals(self.out_picking.state, 'draft')
        self.out_picking.action_confirm()
        self.assertEquals(self.out_picking.state, 'confirmed')
        lot3_vals = {
            'name': 'TestStockProductionLotWithPartner lot 3',
            'product_id': self.product.id}
        lot3 = self.lot_model.create(lot3_vals)
        data = {'product_id': self.product.id,
                'name': self.product.name,
                'product_uom_id': self.product.uom_id.id,
                'location_id': self.out_picking.location_id.id,
                'location_dest_id': self.out_picking.location_dest_id.id,
                'lot_id': lot3.id,
                'qty_done': 5}
        self.out_picking.move_line_ids_without_package = [(0, 0, data)]
        self.out_picking.button_validate()
        self.assertEquals(self.out_picking.state, 'done')
        lot = self.out_picking.move_line_ids_without_package[0].lot_id
        self.assertEquals(lot.name,
                          'TestStockProductionLotWithPartner lot 3')
        self.assertEquals(lot.customer_id.id, self.out_picking.partner_id.id)
