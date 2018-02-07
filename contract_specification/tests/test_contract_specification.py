# Copyright 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl

from odoo.tests import common
from odoo.exceptions import ValidationError


class TestContractSpecification(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestContractSpecification, cls).setUpClass()
        cls.order_condition_obj = cls.env['order.condition']
        cls.number_list_obj = cls.env['number.translation']
        cls.type = cls.env['contract.condition.type'].create({
            'name': 'Test type',
        })
        cls.condition1 = cls.env['contract.condition'].create({
            'name': 'Warranty',
            'description': 'Products are guarantee by manufacturer',
            'type_id': cls.type.id,
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

    def test_number_list_name_get(self):
        number_list = self.number_list_obj.create({
            'name': 'Test list',
            'item_ids': [(0, 0, {'number': 1,
                                 'translation': 'first'})]
        })
        for number_item in number_list.item_ids:
            display_name = '{} - {}'.format(number_item.number,
                                            number_item.translation)
            self.assertEquals(display_name, number_item.display_name)

    def test_unique_selected_per_type(self):
        self.condition1.selected = True
        condition1_copy = self.condition1.copy()
        self.assertFalse(condition1_copy.selected)
        with self.assertRaises(ValidationError):
            condition1_copy.selected = True
