# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, _


class ResPartnerAcademicBackground(models.Model):
    _name = 'res.partner.academic.background'
    _description = 'Academic background'

    def _compute_count_phone_call(self):
        for call in self:
            call.count_phone_call = len(
                call.phone_call_ids)

    phone_call_ids = fields.One2many(
        string='Phone call', inverse_name='academic_background_id',
        comodel_name='crm.phonecall')
    count_phone_call = fields.Integer(
        '# Phone call', compute='_compute_count_phone_call')
    academic_year_id = fields.Many2one(
        string='Academic year', comodel_name='res.partner.academic.year')
    course_level_id = fields.Many2one(
        string='Course level', comodel_name='res.partner.course.level')
    partner_id = fields.Many2one(
        string='Partner', comodel_name='res.partner')
    linguistic_model = fields.Selection(
        [('a', 'A'), ('b', 'B'), ('d', 'D'), ('t', 'T')],
        string='Linguistic model')
    tutor_id = fields.Many2one(string='Tutor', comodel_name='res.partner')
    tutor_phone = fields.Char(
        string='Tutor phone', comodel_name='res.partner',
        related='tutor_id.phone', store=True)
    substitute_id = fields.Many2one(
        string='Substitute', comodel_name='res.partner')
    counselor_id = fields.Many2one(
        string='Counselor', comodel_name='res.partner')
    another_professional_ids = fields.One2many(
        comodel_name='res.partner.another.professional',
        inverse_name='academic_background_id', string='Another professional')
    psychoeducational_report_submitted_id = fields.Many2one(
        string='Psycho-educational report', comodel_name='ir.attachment')
    intervention_plan_delivered_id = fields.Many2one(
        string='Intervention plan', comodel_name='ir.attachment')
    plan_note = fields.Char(string='Plan note')
    contact_note = fields.Char(string='Contact note')

    def action_view_phone_call(self):
        context = self.env.context.copy()
        context.update({'default_academic_background_id': self.id})
        return {
            'name': _("Phone calls"),
            'view_mode': 'tree',
            'res_model': 'crm.phonecall',
            'domain': [('id', 'in', self.phone_call_ids.ids)],
            'type': 'ir.actions.act_window',
            'context': context
        }

    def name_get(self):
        result = []
        for academic_background in self:
            literal = False
            if academic_background.linguistic_model:
                field = academic_background._fields["linguistic_model"]
                literal = field.convert_to_export(
                    academic_background["linguistic_model"],
                    academic_background)
            name = u'{} {} {}'.format(
                academic_background.academic_year_id.name,
                academic_background.course_level_id.name,
                literal or '')
            result.append((academic_background.id, name))
        return result
