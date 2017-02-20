# -*- coding: utf-8 -*-
# © 2017 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common

class TestMrpProduction(common.TransactionCase):

    def setUp(self):
        super(TestMrpProduction, self).setUp()
        self.production = self.env.ref(
            'mrp_operations_extension.mrp_production_opeext')
        operation_index = 0
        operation_ids = []
        product_template = self.production.product_id.product_tmpl_id.id
        values = self.production.product_id.attribute_value_ids.mapped(
            lambda x: {'attribute_id': x.attribute_id.id, 'value_id': x.id,
                       'owner_model': 'mrp.production', 'product_tmpl_id':
                           product_template})
        self.production.product_attribute_ids = map(lambda x: (0, 0, x),
                                                    values)
        for workcenter_line in self.production.routing_id.workcenter_lines:
            workcenter_line.operation = self.env[
                "mrp.routing.operation"].create({'name': "ope{}".format(
                    operation_index)})
            operation_index += 1
            operation_ids.append(workcenter_line.operation.id)
        self.operation_ids = operation_ids

    def test_remove_product_values_related_operations(self):
        self.production.product_id.attribute_value_ids[0].operation_ids = [(
            6, 0, self.operation_ids[:1])]
        self.production.action_compute()
        self.assertEqual(sorted(self.production.workcenter_lines.mapped(
            'routing_wc_line.operation.id')), sorted(self.operation_ids[1:]))

    def test_remove_product_values_related_operations_no_product(self):
        self.production.product_attribute_ids[
            0].value_id.operation_ids = [(6, 0, self.operation_ids[:1])]
        self.production.product_id = self.env['product.product']
        self.production.action_compute()
        self.assertEqual(sorted(self.production.workcenter_lines.mapped(
            'routing_wc_line.operation.id')), sorted(self.operation_ids[1:]))
