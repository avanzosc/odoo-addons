# -*- coding: utf-8 -*-
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests.common import TransactionCase


class TestQcStockInventory(TransactionCase):

    def setUp(self):
        super(TestQcStockInventory, self).setUp()
        self.inv_product = self.env['product.product'].create({
            'name': 'Inventory product',
            'type': 'product',
            'qc_triggers': [
                (0, 0, {'trigger': self.ref('quality_control_stock_inventory.'
                                            'qc_trigger_inventory'),
                        'test': self.ref('quality_control.qc_test_1'),
                        })],
        })
        self.inventory = self.env['stock.inventory'].create({
            'name': 'Inventory test',
            'filter': 'product',
            'product_id': self.inv_product.id,
        })

    def test_inspection_creation(self):
        self.inventory.prepare_inventory()
        self.assertFalse(self.inventory.line_ids)
        self.inventory.write({
            'line_ids': [(0, 0,
                          {'product_id': self.inv_product.id,
                           'product_uom_id':
                           self.ref('product.product_uom_unit'),
                           'product_qty': 10.0,
                           'location_id':
                           self.ref('stock.stock_location_14')})],
        })
        self.inventory.action_done()
        self.assertEquals(self.inventory.state, 'done')
        self.assertEquals(len(self.inventory.line_ids),
                          len(self.inventory.move_ids))
        self.assertNotEquals(self.inventory.created_inspections, 0)
