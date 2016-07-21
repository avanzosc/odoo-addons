# -*- coding: utf-8 -*-
# © 2016 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestProductCalculatedDimensions(common.TransactionCase):

    def setUp(self):
        super(TestProductCalculatedDimensions, self).setUp()
        self.product = self.env.ref('product.product_product_4')
        self.attribute_obj = self.env['product.attribute']
        self.product.product_tmpl_id.volume = 0.0002
        self.product.product_tmpl_id.weight = 0.7
        self.product.volume_formula = "self_t.volume"
        self.product.weight_formula = "self_t.weight " \
                                      "self_p.calculated_volume" \
                                      " num + +"
        self.attribute = self.attribute_obj.create(
            {'attribute_code': 'num',
             'name': 'numeric attr',
             'attr_type': 'numeric',
            })
        values = [{'name': 'value1',
                   'attribute_id': self.attribute.id,
                   'numeric_value': 1},
                  {'name': 'value2',
                   'attribute_id': self.attribute.id,
                   'numeric_value': 2},
                  {'name': 'value3',
                   'attribute_id': self.attribute.id,
                   'numeric_value': 3},
                  ]
        for product, value in zip(self.product.product_variant_ids, values):
            product.write({'attribute_value_ids': [(0, 0, value)]})

    def test_product_dimensions(self):
        for product in self.product.product_variant_ids:
            attr_val = product.attribute_value_ids.filtered(
                lambda x: x.attribute_id.attribute_code == 'num')
            tmpl = product.product_tmpl_id
            self.assertEqual(product.calculated_weight, tmpl.weight +
                             product.calculated_volume +
                             attr_val.numeric_value)
