# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from openerp import exceptions


class TestHrAssistance(common.TransactionCase):

    def setUp(self):
        super(TestHrAssistance, self).setUp()
        self.user = self.env.ref('base.user_demo')
        self.employee = self.env.ref('hr.employee_qdp')
        self.employee_no_user = self.env.ref('hr.employee_vad')

    def test_sign_in(self):
        self.assertEqual(self.employee.state, 'absent')
        self.user.register_pass = '1234'
        wiz = self.env['employee.register.wiz'].with_context({
            'active_id': self.employee.id}).create({})
        wiz.register_pass = '123'
        with self.assertRaises(exceptions.Warning):
            wiz.sign_in_employee()
        wiz.register_pass = '1234'
        wiz.sign_in_employee()
        self.assertEqual(self.employee.state, 'present')
        wiz2 = self.env['employee.register.wiz'].with_context({
            'active_id': self.employee_no_user.id}).create({})
        with self.assertRaises(exceptions.Warning):
            wiz2.sign_in_employee()
