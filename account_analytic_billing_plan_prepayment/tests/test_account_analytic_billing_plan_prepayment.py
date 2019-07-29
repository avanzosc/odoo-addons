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
        prepayment_type = cls.env.ref('account.data_account_type_prepayments')
        accounts = cls.product2.product_tmpl_id.get_product_accounts()
        accounts.get('income').user_type_id = prepayment_type

    def test_check_prepayment_final_invoice(self):
        self.assertTrue(self.plan2.prepayment)
        with self.assertRaises(ValidationError):
            self.plan2.final_invoice = True
