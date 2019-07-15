# -*- coding: utf-8 -*-
# Copyright (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestProductTrainingPlan(common.TransactionCase):

    def setUp(self):
        super(TestProductTrainingPlan, self).setUp()
        self.training_plan_model = self.env['training.plan']
        self.product_plan_model = self.env['product.training.plan']
        self.sequence_model = ['ir.sequence']
        self.product = self.env['product.product'].create({
            'name': 'test product',
        })

    def test_product_training_plan(self):
        vals = {'name': 'Training plan for test'}
        training_plan = self.training_plan_model.create(vals)
        category = self.browse_ref(
            'product_training_plan.training_plan_category1')
        self.assertEqual(training_plan.category_id.name,
                         category.name,
                         'Bad training plan category')
        new_training_plan = training_plan.copy()
        sequence = self.browse_ref(
            'product_training_plan.training_plan_sequence')
        sequence_number = sequence.number_next_actual - 1
        self.assertIn(
            str(sequence_number), new_training_plan.code,
            'Bad sequence after copy training plan')
        search_by_name = self.training_plan_model.name_search(
            name=new_training_plan.code)
        self.assertIn((new_training_plan.id, new_training_plan.name),
                      search_by_name)

    def test_product_training_plans(self):
        plan1 = self.training_plan_model.create({
            'name': 'Plan 1',
        })
        plan2 = self.training_plan_model.create({
            'name': 'Plan 2',
        })
        self.product_plan_model.create({
            'product_tmpl_id': self.product.product_tmpl_id.id,
            'training_plan_id': plan1.id,
        })
        self.product_plan_model.create({
            'product_tmpl_id': self.product.product_tmpl_id.id,
            'product_id': self.product.id,
            'training_plan_id': plan2.id,
        })
        self.assertTrue(len(self.product.product_training_ids) == 1)
        self.assertTrue(len(self.product.template_training_ids) == 1)
        self.assertTrue(
            len(self.product.product_tmpl_id
                .product_template_training_ids) == 2)
