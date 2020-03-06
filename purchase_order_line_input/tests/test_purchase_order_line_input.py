# Copyright 2018 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common, SavepointCase


@common.at_install(False)
@common.post_install(True)
class TestPurchaseOrderLineInput(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.purchase_line_model = cls.env['purchase.order.line']
        cls.partner = cls.env['res.partner'].create({'name': 'Test'})
        cls.product = cls.env['product.product'].create({
            'name': 'test_product',
            'type': 'service',
        })

    def test_purchase_order_create_and_show(self):
        new_line = self.purchase_line_model.new({
            'partner_id': self.partner.id,
            'product_id': self.product.id,
            'product_qty': 8.0,
            'product_uom': self.product.uom_id.id,
            'price_unit': 190.50,
            'name': 'Test line description',
        })
        new_line._onchange_quantity()
        line_data = new_line._convert_to_write(new_line._cache)
        line = self.purchase_line_model.create(line_data)
        self.assertTrue(line.order_id)
        action_dict = line.action_purchase_order_form()
        self.assertEquals(action_dict['res_id'], line.order_id.id)
        self.assertEquals(action_dict['res_model'], 'purchase.order')
        order_action_dict = line.order_id.action_view_lines()
        self.assertEquals(
            order_action_dict["domain"],
            "[('order_id', '=', {})]".format(line.order_id.id))
