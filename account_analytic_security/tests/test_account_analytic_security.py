# -*- coding: utf-8 -*-
# © 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestAccountAnalyticSecurity(common.TransactionCase):

    def setUp(self):
        super(TestAccountAnalyticSecurity, self).setUp()
        self.user_obj = self.env['res.users']
        self.user = self.user_obj.create({
            'name': 'Test',
            'login': 'test',
        })
        self.partner_obj = self.env['res.partner']
        self.partner = self.partner_obj.create({
            'name': 'Partner test'
        })
        self.public_project = self.env.ref('project.project_project_1')
        self.project = self.env.ref('project.project_project_2')

    def test_members(self):
        self.assertFalse(self.public_project.analytic_account_id.partner_ids)
        self.project.members = [(4, self.user.id)]
        self.assertTrue(self.project.analytic_account_id.partner_ids)
        self.assertTrue(
            True for partner in self.project.analytic_account_id.partner_ids
            if partner == self.user.partner_id)
        self.project.message_follower_ids = [(4, self.partner.id)]
        self.assertTrue(
            True for partner in self.project.analytic_account_id.partner_ids
            if partner == self.partner_id)
