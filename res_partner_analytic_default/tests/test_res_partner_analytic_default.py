# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestResPartnerAnalyticDefault(common.TransactionCase):

    def setUp(self):
        super(TestResPartnerAnalyticDefault, self).setUp()
        vals = {'name': 'New customer for test',
                'is_company': True,
                'customer': True,
                'company_id': self.env.user.company_id.id}
        self.customer = self.env['res.partner'].create(vals)

    def test_crm_claim_filter(self):
        self.assertNotEqual(
            self.customer.analytic_default, False,
            'Customer created without default analytic account')
