# -*- coding: utf-8 -*-
# © 2016 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestProductCalculatedDimensions(common.TransactionCase):

    def setUp(self):
        super(TestProductCalculatedDimensions, self).setUp()
        self.product = self.env.ref('product.product_product_4')
        self.attribute_obj = self.env['product.attribute']
        tmpl = self.product.product_tmpl_id
        tmpl.volume = 0.0002
        tmpl.weight = 0.7
        self.product.custom_uos_coeff = "7"
        self.product.custom_uop_coeff = "13"
        tmpl.volume_formula = "self_t.volume"
        tmpl.weight_formula = "self_t.weight " \
                              "self_p.calculated_volume " \
                              "num + - 4 /"
        tmpl.weight_net_formula = "num 2 *"
        tmpl.uos_coeff_formula = "num 3 *"
        tmpl.uop_coeff_formula = "num 4 *"
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
            numeric_value = product.attribute_value_ids.filtered(
                lambda x: x.attribute_id.attribute_code == 'num').numeric_value
            tmpl = product.product_tmpl_id
            self.assertEqual(product.calculated_volume, tmpl.volume)
            self.assertEqual(product.calculated_weight, (tmpl.weight -
                             (product.calculated_volume + numeric_value)) / 4)
            self.assertEqual(product.calculated_weight_net, numeric_value * 2)
            self.assertEqual(product.uos_coeff, numeric_value * 3)
            self.assertEqual(product.uop_coeff, numeric_value * 4)

            product.custom_uos_coeff_check = True
            product.compute_uos_coeff()
            if product == self.product:
                self.assertEqual(product.uos_coeff, 7)
            else:
                self.assertEqual(product.uos_coeff, 1)
            product.custom_uos_coeff_check = False
            product.compute_uos_coeff()
            self.assertEqual(product.uos_coeff, numeric_value * 3)
            product.custom_uop_coeff_check = True
            product.compute_uop_coeff()
            if product == self.product:
                self.assertEqual(product.uop_coeff, 13)
            else:
                self.assertEqual(product.uop_coeff, 1)
            product.custom_uop_coeff_check = False
            product.compute_uop_coeff()
            self.assertEqual(product.uop_coeff, numeric_value * 4)

            product.uos_coeff_formula = "0"
            product.uop_coeff_formula = "0"
            product.custom_uos_coeff = "0"
            product.custom_uop_coeff = "0"
            self.assertEqual(product.uos_coeff, 1)
            self.assertEqual(product.uop_coeff, 1)

            product.uos_coeff_formula = "num 3 *"
            product.uop_coeff_formula = "num 4 *"
            self.assertEqual(product.uos_coeff, numeric_value * 3)
            self.assertEqual(product.uop_coeff, numeric_value * 4)
            product.custom_uos_coeff_check = True
            product.compute_uos_coeff()
            self.assertEqual(product.uos_coeff, 1)
            product.custom_uop_coeff_check = True
            product.compute_uop_coeff()
            self.assertEqual(product.uop_coeff, 1)
