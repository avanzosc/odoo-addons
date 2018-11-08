# -*- coding: utf-8 -*-
# Copyright 2018 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, models


class ResGroups(models.Model):
    _inherit = "res.groups"

    @api.multi
    def duplicate_group(self):
        self.ensure_one()
        new_id = self.copy({'name': self.name + u'_new'})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.groups',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'current',
            'res_id': new_id.id,
            # 'views': self.env.ref('base.view_groups_form').id,
        }
