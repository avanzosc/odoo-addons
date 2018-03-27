# -*- coding: utf-8 -*-
# Copyright © 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.multi
    def _copy_administrator_permissions(self):
        user_root = self.env.ref('base.user_root', False)
        if user_root:
            self.copy_administrator_permissions(user_root)

    @api.multi
    def copy_administrator_permissions(self, user_root):
        groups_obj = self.env['res.groups']
        for user in self:
            cond = [('users', 'in', (user.id))]
            user_groups = groups_obj.search(cond)
            user_groups.write({'users': [(3, user.id)]})
            cond = [('users', 'in', (user_root.id))]
            admin_groups = groups_obj.search(cond)
            admin_groups.write({'users': [(4, user.id)]})
