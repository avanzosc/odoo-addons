# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    student_meetings_ids = fields.One2many(
        comodel_name='calendar.event',
        inverse_name='student_id', string='Tutoring meetings')
    student_count_meetings = fields.Integer(
        string='# Tutoring meetings',
        compute='_compute_student_count_meetings')
    family_meetings_ids = fields.One2many(
        comodel_name='calendar.event',
        inverse_name='family_id', string='Tutoring meetings')
    family_count_meetings = fields.Integer(
        string='# Tutoring meetings',
        compute='_compute_family_count_meetings')

    def _compute_student_count_meetings(self):
        for partner in self:
            partner.student_count_meetings = (
                len(partner.student_meetings_ids))

    def _compute_family_count_meetings(self):
        for partner in self:
            partner.family_count_meetings = (
                len(partner.family_meetings_ids))

    @api.multi
    def button_show_student_meetings(self):
        self.ensure_one()
        self = self.with_context(
            search_default_student_id=self.id, default_student_id=self.id)
        return {'name': _('Tutoring meetings'),
                'type': 'ir.actions.act_window',
                'view_mode': 'calendar,tree,form',
                'view_type': 'form',
                'res_model': 'calendar.event',
                'domain': [('id', 'in', self.student_meetings_ids.ids)],
                'context': self.env.context}

    @api.multi
    def button_show_family_meetings(self):
        self.ensure_one()
        self = self.with_context(
            search_default_family_id=self.id,
            default_family_id=self.id)
        return {'name': _('Tutoring meetings'),
                'type': 'ir.actions.act_window',
                'view_mode': 'calendar,tree,form',
                'view_type': 'form',
                'res_model': 'calendar.event',
                'domain': [('id', 'in', self.family_meetings_ids.ids)],
                'context': self.env.context}
