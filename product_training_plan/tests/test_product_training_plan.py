# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestProductTrainingPlan(common.TransactionCase):

    def setUp(self):
        super(TestProductTrainingPlan, self).setUp()
        self.training_plan_model = self.env['training.plan']
        self.sequence_model = ['ir.sequence']

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
            str(sequence_number), new_training_plan.sequence,
            'Bad sequence after copy training plan')
