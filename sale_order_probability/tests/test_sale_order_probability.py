# Copyright 2020 Adrian Revilla - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestSaleOrderProbability(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestSaleOrderProbability, cls).setUpClass()
        cls.sale_order_model = cls.env['sale.order']
        cls.res_partner_model = cls.env['res.partner']
        cls.product_product_model = cls.env['product.product']

        cls.res_partner_1 = cls.res_partner_model.create({
            'firstname': 'Partner 1'
        })
        cls.product_product_1 = cls.product_product_model.create({
            'name': 'Product 1',
            'lst_price': 100.0
        })
        cls.sale_order_1 = cls.sale_order_model.create({
            'partner_id': cls.res_partner_1.id,
            'planned_percentage': 0.5,
        })

    def test_sale_order_probability(self):
        self.sale_order_1._compute_probability_percentage()
        self.assertEquals(self.sale_order_1.probability_percentage, 0.0)
