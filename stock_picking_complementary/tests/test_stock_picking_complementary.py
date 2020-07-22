# Copyright 2020 Mikel Arregi - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class StockPickingComplementaryTest(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(StockPickingComplementaryTest, cls).setUpClass()
        cls.stock_picking_model = cls.env['stock.picking']
        cls.partner_model = cls.env['res.partner']
        cls.location_model = cls.env['stock.location']
        cls.stock_move_model = cls.env['stock.move']
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.product_model = cls.env['product.product']
        cls.stock_picking_type_model = cls.env['stock.picking.type']
        cls.location1 = cls.location_model.create({
            'name': 'Location1'
        })
        cls.location2 = cls.location_model.create({
            'name': 'Location2'
        })
        cls.location3 = cls.location_model.create({
            'name': 'Location3'
        })
        cls.partner = cls.partner_model.create({
            'name': 'Partner1',
        })
        cls.stock_picking_type = cls.stock_picking_type_model.create(
            {'name': 'test',
             'sequence_id': 1,
             'code': 'outgoing'})
        cls.stock_picking_type = cls.stock_picking_type_model.create(
            {'name': 'test',
             'sequence_id': 1,
             'code': 'internal'})
        cls.stock_picking = cls.stock_picking_model.create({
            'res_partner': cls.partner,
            'location_id': cls.location1.id,
            'location_dest_id': cls.location2.id,
            'show_check_availability': True,
            'picking_type_id': cls.stock_picking_type.id,
        })
        cls.product = cls.product_model.create({
            'name': 'Product',
            'default_code': 'P1',
            'uom_id': cls.uom_unit.id,
        })

    def test_complementary_stock_picking(self):
        self.stock_picking.move_ids_without_package = \
            self.stock_move_model.new({
                'name': "Move1",
                'product_id': self.product.id,
                'product_uom_qty': 5,
                'product_uom': self.uom_unit.id,
                'picking_id': self.stock_picking.id,
                'location_id': self.location1.id,
                'location_dest_id': self.location2.id,
            })
        new_picking_id = self.stock_picking.create_complementary_picking(
            location_id=self.location3)[0][1]
        new_line = new_picking_id.move_ids_without_package[0]
        self.assertEqual(new_line.product_uom_qty, 5)
        self.assertEqual(new_line.location_id, self.location3)
        self.assertEqual(new_line.location_dest_id, self.location1)
