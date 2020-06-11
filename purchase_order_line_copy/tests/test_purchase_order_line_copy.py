# Copyright 2020 Mikel Arregi - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class PurchaseOrderLineProductConfiguratorTest(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(PurchaseOrderLineProductConfiguratorTest, cls).setUpClass()
        cls.product_model = cls.env['product.product']
        cls.partner_model = cls.env['res.partner']
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.purchase_line_obj = cls.env['purchase.order.line']
        cls.partner = cls.partner_model.create({
            'name': 'Partner1',
        })
        cls.purhcase_order = cls.env['purchase.order'].create({
            'partner_id': cls.partner.id,
        })
        cls.product = cls.product_model.create({
            'name': 'Product',
            'default_code': 'P1',
            'uom_id': cls.uom_unit.id,
        })

    def test_copy_purchase_order_line(self):
        new_line = self.purchase_line_obj.new(
            {'name': 'test',
             'order_id': self.purhase_order.id,
             'product_id': self.product.id,
             'product_uom_qty': 2,
             })
        self.purchase_order.order_line = new_line
        self.purchase_order.order_line.copy_purchase_order_line()
        self.assertEqual(len(self.purchase_order.order_line), 2)
