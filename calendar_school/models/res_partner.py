# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class ResPartner(models.Model):
    _inherit = 'res.partner'

    student_meeting_ids = fields.One2many(
        comodel_name='calendar.event',
        inverse_name='student_id', string='Tutoring meetings (student)')
    student_count_meetings = fields.Integer(
        string='# Tutoring meetings (student)',
        compute='_compute_student_count_meetings')
    family_meeting_ids = fields.One2many(
        comodel_name='calendar.event',
        inverse_name='family_id', string='Tutoring meetings (family)')
    family_count_meetings = fields.Integer(
        string='# Tutoring meetings (family)',
        compute='_compute_family_count_meetings')

    @api.depends("year_tutor_ids", "year_tutor_ids.substitute_id")
    def _compute_current_year_tutor_ids(self):
        super(ResPartner, self)._compute_current_year_tutor_ids()
        for partner in self:
            tutors = partner.sudo().year_tutor_ids.filtered(
                lambda t: t.school_year_id.current and t.substitute_id)
            partner.current_year_tutor_ids |= tutors.mapped("substitute_id")

    def _compute_student_count_meetings(self):
        calendar_obj = self.env['calendar.event']
        for partner in self:
            partner.student_count_meetings = calendar_obj.search_count([
                ('student_id', '=', partner.id)])

    def _compute_family_count_meetings(self):
        calendar_obj = self.env['calendar.event']
        for partner in self:
            partner.family_count_meetings = calendar_obj.search_count([
                ('family_id', '=', partner.id)])

    @api.multi
    def button_show_meetings(self):
        self.ensure_one()
        action = self.env.ref('calendar.action_calendar_event')
        action_dict = action.read()[0] if action else {}
        action_dict['context'] = safe_eval(
            action_dict.get('context', '{}'))
        domain = safe_eval(action.domain or '[]')
        if self.educational_category == 'student':
            action_dict['context'].update({
                'search_default_student_id': self.id,
                'default_student_id': self.id,
            })
            domain = expression.AND([
                [('student_id', 'in', self.ids)], domain])
        elif self.educational_category == 'family':
            action_dict['context'].update({
                'search_default_family_id': self.id,
                'default_family_id': self.id,
            })
            domain = expression.AND([
                [('family_id', 'in', self.ids)], domain])
        action_dict.update({'domain': domain})
        return action_dict
