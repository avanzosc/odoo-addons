# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestHrEmployeeCatchPartner(common.TransactionCase):

    def setUp(self):
        super(TestHrEmployeeCatchPartner, self).setUp()
        self.employee_model = self.env['hr.employee']
        employee_vals = {'name': 'employee name',
                         'user_id':  self.ref('base.user_root')}
        self.employee = self.employee_model.create(employee_vals)

    def test_hr_employee_catch_partner(self):
        result = self.employee.onchange_user(self.ref('base.user_root'))
        self.assertNotEqual(
            result.get('value', False), False, 'Value not found in result')
        self.assertNotEqual(
            result['value'].get('address_home_id', False), False,
            'Partner not found')
