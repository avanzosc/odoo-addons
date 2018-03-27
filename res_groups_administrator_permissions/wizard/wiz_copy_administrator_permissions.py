# -*- coding: utf-8 -*-
# Copyright © 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class WizCopyAdministratorPermissions(models.TransientModel):
    _name = 'wiz.copy.administrator.permissions'

    @api.multi
    def action_copy_admin_permissions(self):
        self.ensure_one()
        for user in self.env['res.users'].browse(
                self.env.context.get('active_ids')):
            user._copy_administrator_permissions()
