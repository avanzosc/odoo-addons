# -*- coding: utf-8 -*-
# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _compute_num_347_records(self):
        record_obj = self.env['l10n.es.aeat.mod347.partner_record']
        for partner in self:
            cond = [('partner_id', '=', partner.id)]
            partner.num_347_records = len(record_obj.search(cond))

    num_347_records = fields.Integer(
        string='AEAT 347 partner records', compute='_compute_num_347_records')

    @api.multi
    def show_partner_347_records(self):
        res = {'view_mode': 'tree,form',
               'res_model': 'l10n.es.aeat.mod347.partner_record',
               'view_id': False,
               'type': 'ir.actions.act_window',
               'view_type': 'form',
               'domain': [('partner_id', '=', self.id)],
               'context': {'tree_view_ref': 'l10n_es_aeat_mod347_ext.l10n_es_'
                           'aeat_mod347_partner_record_tree_view'}}
        return res
