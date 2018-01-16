# Copyright 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl

from odoo.tests import common


class TestContractSpecification(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestContractSpecification, cls).setUpClass()
        cls.order_condition_obj = cls.env['order.condition']
        cls.condition1 = cls.env['contract.condition'].create({
            'name': 'Warranty',
            'description': 'Products are guarantee by manufacturer',
        })
        cls.condition2 = cls.env['contract.condition'].create({
            'name': 'Warranty',
        })

    def test_onchange_condition_id(self):
        order_condition = self.order_condition_obj.new({
            'condition_id': self.condition1.id,
        })
        self.assertFalse(order_condition.description)
        order_condition._onchange_condition_id()
        self.assertEquals(order_condition.description,
                          self.condition1.description)
        order_condition.condition_id = self.condition2.id
        order_condition._onchange_condition_id()
        self.assertEquals(order_condition.description,
                          self.condition2.name)
