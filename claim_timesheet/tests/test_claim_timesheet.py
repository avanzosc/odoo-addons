# -*- coding: utf-8 -*-
# (Copyright) 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestClaimTimesheet(common.TransactionCase):

    def setUp(self):
        super(TestClaimTimesheet, self).setUp()
        self.crm_claim = self.env.ref('crm_claim.crm_claim_2')
        self.project = self.env.ref('project.project_project_5')
        self.analytic_timesheet_obj = self.env['hr.analytic.timesheet']
        self.user = self.env.ref('base.user_root')
        self.analytic = self.project.analytic_account_id

    def test_onchange(self):
        self.analytic.use_timesheets = True
        self.assertFalse(self.crm_claim.analytic_id)
        self.crm_claim.project_id = self.project
        self.assertTrue(self.crm_claim.analytic_id)
        self.assertFalse(self.crm_claim.timesheet_ids)
        timesheet = self.analytic_timesheet_obj.create({
            'name': 'Testing',
            'user_id': self.user.id,
            'journal_id': self.env.ref('hr_timesheet.analytic_journal').id,
            'account_id': self.project.analytic_account_id.id,
            'claim_id': self.crm_claim.id,
        })
        self.assertTrue(timesheet)
        self.assertTrue(self.crm_claim.timesheet_ids)
