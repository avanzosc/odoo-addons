# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestResPartnerAnalytic(common.TransactionCase):

    def setUp(self):
        super(TestResPartnerAnalytic, self).setUp()
        self.analytic_default_model = self.env['account.analytic.default']
        vals = {
            'name': 'Test Customer',
            'is_company': True,
            'customer': True,
            'company_id': self.env.user.company_id.id,
        }
        self.customer = self.env['res.partner'].create(vals)

    def test_res_partner_analytic(self):
        analytic = self.analytic_default_model.search(
            [('partner_id', '=', self.customer.id)])
        self.assertNotEqual(
            len(analytic), 0, 'Created analytic distribution')
