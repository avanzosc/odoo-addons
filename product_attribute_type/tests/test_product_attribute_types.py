# Copyright 2015 Oihane Crucelaegui - AvanzOSC
# Copyright 2015-2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2018 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import odoo.tests.common as common


class TestProductAttributeTypes(common.TransactionCase):

    def setUp(self):
        super(TestProductAttributeTypes, self).setUp()
        self.attribute_model = self.env['product.attribute']
        self.attribute_value_model = self.env['product.attribute.value']
        self.attribute = self.attribute_model.create(
            {
                'name': 'attr1',
                'attr_type': 'numeric'
            }
        )
        self.attribute_value = self.attribute_value_model.create(
            {
                'name': 'value1',
                'attribute_id': self.attribute.id
            }
        )

    def test_onchange_numeric_value_name(self):
        self.attribute_value.name = '3'
        self.attribute_value.onchange_name()
        self.assertEquals(self.attribute_value.numeric_value,
                          float(self.attribute_value.name),
                          'Numeric value properly assigned')
