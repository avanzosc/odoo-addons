# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class ResPartner(models.Model):

    _inherit = 'res.partner'

    @api.multi
    def _count_session(self):
        for partner in self:
            partner.session_count = len(partner.sessions)

    sessions = fields.Many2many(
        comodel_name="event.track", relation="rel_partner_event_track",
        column1="partner_id", column2="event_track_id", string="Sessions",
        copy=False)
    session_count = fields.Integer(
        string='Sessions counter', compute='_count_session')

    @api.multi
    def show_sessions_from_partner(self):
        res = {'view_mode': 'kanban,tree,form,calendar,graph',
               'res_model': 'event.track',
               'view_id': False,
               'type': 'ir.actions.act_window',
               'view_type': 'form',
               'domain': [('id', 'in', self.sessions.ids)]}
        return res
