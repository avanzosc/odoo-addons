# -*- coding: utf-8 -*-
# Copyright © 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestResGroupsAdministratorPermissions(common.TransactionCase):

    def setUp(self):
        super(TestResGroupsAdministratorPermissions, self).setUp()
        self.groups_obj = self.env['res.groups']
        self.user = self.env['res.users'].create({
            'name': 'User for test copy administrator permissions',
            'login': 'usercopy@test.com'})

    def test_res_groups_administrator_permissions(self):
        wiz = self.env['wiz.copy.administrator.permissions'].create({})
        wiz.with_context(
            active_ids=[self.user.id]).action_copy_admin_permissions()
        user_root = self.env.ref('base.user_root', False)
        cond = [('users', 'in', (user_root.id))]
        admin_groups = self.groups_obj.search(cond)
        cond = [('users', 'in', (self.user.id))]
        user_groups = self.groups_obj.search(cond)
        self.assertEquals(len(admin_groups), len(user_groups),
                          'Bad permission for user')
