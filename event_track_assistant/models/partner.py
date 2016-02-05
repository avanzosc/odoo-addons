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

    @api.multi
    def _count_presences(self):
        for partner in self:
            partner.presences_count = len(partner.presences)

    sessions = fields.Many2many(
        comodel_name="event.track", relation="rel_partner_event_track",
        column1="partner_id", column2="event_track_id", string="Sessions",
        copy=False)
    session_count = fields.Integer(
        string='Sessions counter', compute='_count_session')
    presences = fields.One2many(
        comodel_name='event.track.presence', inverse_name='partner',
        string='Presences')
    presences_count = fields.Integer(
        string='Presences counter', compute='_count_presences')

    @api.multi
    def show_sessions_from_partner(self):
        res = {'view_mode': 'kanban,tree,form,calendar,graph',
               'res_model': 'event.track',
               'view_id': False,
               'type': 'ir.actions.act_window',
               'view_type': 'form',
               'domain': [('id', 'in', self.sessions.ids)]}
        return res

    @api.multi
    def show_presences_from_partner(self):
        res = {'view_mode': 'tree,form',
               'res_model': 'event.track.presence',
               'view_id': False,
               'type': 'ir.actions.act_window',
               'view_type': 'form',
               'domain': [('partner', '=', self.id)]}
        return res
