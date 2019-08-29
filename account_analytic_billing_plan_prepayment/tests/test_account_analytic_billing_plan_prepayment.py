# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo.exceptions import ValidationError
from odoo.addons.account_analytic_billing_plan.tests\
    .test_account_analytic_billing_plan import TestAccountAnalyticBillingPlan


@common.at_install(False)
@common.post_install(True)
class TestAccountAnalyticBillingPlanPrepayment(TestAccountAnalyticBillingPlan):

    @classmethod
    def setUpClass(cls):
        super(TestAccountAnalyticBillingPlanPrepayment, cls).setUpClass()
        revenue_type = cls.env.ref('account.data_account_type_revenue')
        prepayment_type = cls.env.ref('account.data_account_type_prepayments')
        cls.account_model = cls.env['account.account']
        cls.product1.property_account_income_id = cls.account_model.create({
            'code': 'NewAccount1',
            'name': 'Test Account',
            'user_type_id': revenue_type.id,
        })
        cls.product2.property_account_income_id = cls.account_model.create({
            'code': 'NewAccount2',
            'name': 'Test Account Prepayment',
            'user_type_id': prepayment_type.id,
        })

    def test_check_prepayment_final_invoice(self):
        self.assertTrue(self.plan2.prepayment)
        with self.assertRaises(ValidationError):
            self.plan2.final_invoice = True

    def test_final_invoice(self):
        self.assertFalse(self.plan1.prepayment)
        self.plan1.final_invoice = True
        self.assertFalse(self.plan2.prepayment_amount)
        self.plan2.action_invoice_create()
        self.assertTrue(self.plan2.prepayment_amount)
        self.plan1.action_invoice_create()
        self.assertFalse(self.plan2.prepayment_amount)
