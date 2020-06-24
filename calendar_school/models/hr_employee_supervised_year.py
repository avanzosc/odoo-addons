# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval
from datetime import timedelta


class HrEmployeeSupervisedYear(models.Model):
    _inherit = 'hr.employee.supervised.year'

    center_id = fields.Many2one(
        comodel_name='res.partner', string='Education Center',
        compute='_compute_education_info', store=True)
    course_id = fields.Many2one(
        comodel_name='education.course', string='Education Course',
        compute='_compute_education_info', store=True)
    meeting_ids = fields.One2many(
        comodel_name='calendar.event', inverse_name='supervised_year_id',
        string='Meetings')
    count_meetings = fields.Integer(
        string='# Tutoring meetings', compute='_compute_count_meetings')
    substitution_ids = fields.One2many(
        string='Substitutions', inverse_name='supervised_year_id',
        comodel_name='hr.employee.supervised.year.substitution')

    @api.depends('student_id', 'student_id.student_group_ids',
                 'student_id.student_group_ids.group_type_id',
                 'student_id.student_group_ids.group_type_id.type',
                 'student_id.student_group_ids.center_id',
                 'student_id.student_group_ids.course_id', 'school_year_id')
    def _compute_education_info(self):
        for year in self:
            groups = year.student_id.student_group_ids.filtered(
                lambda g: g.group_type_id.type == 'official' and
                g.academic_year_id == year.school_year_id
            )
            year.center_id = groups[:1].center_id
            year.course_id = groups[:1].course_id

    @api.depends('meeting_ids')
    def _compute_count_meetings(self):
        for year in self:
            year.count_meetings = (len(year.meeting_ids))

    @api.multi
    def button_show_meetings(self):
        self.ensure_one()
        action = self.env.ref('calendar.action_calendar_event')
        action_dict = action.read()[0] if action else {}
        action_dict['context'] = safe_eval(
            action_dict.get('context', '{}'))
        action_dict['context'].update({
            'search_default_supervised_year_id': self.id,
            'default_supervised_year_id': self.id,
            'search_default_teacher_id': self.teacher_id.id,
            'default_teacher_id': self.teacher_id.id,
            'search_default_student_id': self.student_id.id,
            'default_student_id': self.student_id.id,
        })
        domain = expression.AND([
            [('supervised_year_id', 'in', self.ids)],
            safe_eval(action.domain or '[]')])
        action_dict.update({'domain': domain})
        return action_dict

    @api.multi
    def generate_meetings(self):
        for supervised in self:
            if not supervised.center_id or not supervised.course_id:
                break
            school_year = supervised.school_year_id
            if not school_year.date_start or not school_year.date_end:
                break
            date = school_year.date_start
            while date <= school_year.date_end:
                agenda = self._get_meeting_agenda(date, 'student')
                if (bool(agenda) and not supervised._has_event(date)):
                    supervised._create_calendar_event(date)
                agenda = self._get_meeting_agenda(date, 'family')
                if bool(agenda):
                    for family in supervised.student_id.mapped(
                            'child2_ids.family_id'):
                        if not supervised._has_event(date, family):
                            supervised._create_calendar_event(date, family)
                date += timedelta(days=1)

    def _has_event(self, date, family=False):
        start = fields.Datetime.to_datetime(date)
        cond = [('supervised_year_id', '=', self.id),
                ('center_id', '=', self.center_id.id),
                ('course_id', '=', self.course_id.id),
                ('teacher_id', '=', self.teacher_id.id),
                ('student_id', '=', self.student_id.id),
                ('family_id', '=', family and family.id),
                ('start', '>=', start),
                ('start', '<=', start.replace(hour=23, minute=59, second=59))]
        return bool(self.env['calendar.event'].search(cond, limit=1))

    def _get_meeting_agenda(self, date, meeting_type):
        agenda_text = ''
        if meeting_type and self.center_id and self.course_id:
            month = self.env['base.month'].search([
                ('number', '=', date.month)])
            cond = [('school_id', '=', self.center_id.id),
                    ('course_id', '=', self.course_id.id),
                    ('type', '=', meeting_type),
                    ('month_id', '=', month.id),
                    ('meeting_day', '=', str(date.day))]
            agendas = self.env['education.order.day'].search(cond)
            if agendas:
                agenda_text = u"\n".join(agendas.mapped('order_day'))
        return agenda_text

    def _catch_meeting_values(
            self, date, hour, duration, meeting_type, family=False):
        self.ensure_one()
        date = fields.Datetime.to_datetime(date)
        day = fields.Datetime.context_timestamp(
            self, date)
        start = day.replace(hour=hour) - day.utcoffset()
        stop = start + timedelta(minutes=duration)
        alarm = self.env.ref('calendar.alarm_notif_5')
        name = _('Meeting')
        label = self.env['calendar.event.type']
        partners = self.teacher_id.user_id.partner_id
        if meeting_type == 'student':
            name = _(u'Student {} Meeting').format(self.student_id.name)
            label = self.env.ref(
                'calendar_school.calendar_event_type_student_tutoring')
            partners |= self.student_id
        elif meeting_type == 'family':
            name = _(u'Family {} Meeting').format(
                family.name if family else '')
            label = self.env.ref(
                'calendar_school.calendar_event_type_family_tutoring')
            partners |= family.family_ids.filtered(
                lambda f: f.child2_id == self.student_id).mapped(
                'responsible_id')
        vals = {
            'name': name,
            'supervised_year_id': self.id,
            'student_id': self.student_id.id,
            'teacher_id': self.teacher_id.id,
            'family_id': family and family.id,
            'allday': False,
            'start': fields.Datetime.to_string(start),
            'stop': fields.Datetime.to_string(stop),
            'user_id': self.teacher_id.user_id.id or self.env.user.id,
            'alarm_ids': [(6, 0, alarm.ids)],
            'partner_ids': [(6, 0, partners.ids)],
            'categ_ids': [(6, 0, label.ids)],
            'agenda': self._get_meeting_agenda(date, meeting_type),
            'center_id': self.center_id.id,
            'course_id': self.course_id.id
        }
        return vals

    def _create_calendar_event(self, date, family=False):
        self.ensure_one()
        hour = 9
        duration = 15
        meeting_type = 'student'
        if family:
            hour = 15
            duration = 30
            meeting_type = 'family'
        vals = self._catch_meeting_values(
            date, hour, duration, meeting_type, family=family)
        vals.update({
            'res_id': self.id,
            'res_model': self._name,
            'res_model_id': self.env['ir.model']._get_id(self._name),
        })
        calendar = self.env['calendar.event'].create(vals)
        return calendar


class HrEmployeeSupervisedYearSubstitution(models.Model):
    _name = 'hr.employee.supervised.year.substitution'
    _description = 'Supervised year substitutions'

    supervised_year_id = fields.Many2one(
        comodel_name='hr.employee.supervised.year', string='Supervised')
    from_date = fields.Date(string='Substitute teacher from')
    to_date = fields.Date(string='Substitute teacher until')
    substitute_teacher_id = fields.Many2one(
        string='Teacher making the substitution', comodel_name='hr.employee')

    @api.model
    def create(self, values):
        label_student = self.env.ref(
            'calendar_school.calendar_event_type_student_tutoring')
        label_family = self.env.ref(
            'calendar_school.calendar_event_type_family_tutoring')
        substitution = super(
            HrEmployeeSupervisedYearSubstitution, self).create(values)
        calendars = substitution._search_calendars()
        for calendar in calendars:
            partner = substitution.substitute_teacher_id.user_id.partner_id
            if ((label_student.id in calendar.categ_ids.ids or
                label_family.id in calendar.categ_ids.ids) and
                    partner.id not in calendar.partner_ids.ids):
                calendar.partner_ids = [(4, partner.id)]
        return substitution

    @api.multi
    def unlink(self):
        label_student = self.env.ref(
            'calendar_school.calendar_event_type_student_tutoring')
        label_family = self.env.ref(
            'calendar_school.calendar_event_type_family_tutoring')
        for substitution in self:
            calendars = substitution._search_calendars()
            for calendar in calendars:
                partner = substitution.substitute_teacher_id.user_id.partner_id
                if ((label_student.id in calendar.categ_ids.ids or
                    label_family.id in calendar.categ_ids.ids) and
                        partner.id in calendar.partner_ids.ids):
                    calendar.partner_ids = [(3, partner.id)]
        return super(HrEmployeeSupervisedYearSubstitution, self).unlink()

    def _search_calendars(self):
        from_date = '{} 00:00:00'.format(self.from_date)
        to_date = '{} 23:59:59'.format(self.to_date)
        cond = [('supervised_year_id', '=', self.supervised_year_id.id),
                ('teacher_id', '=', self.supervised_year_id.teacher_id.id),
                ('start', '>=', from_date),
                ('start', '<=', to_date),
                ('student_id', '=', self.supervised_year_id.student_id.id)]
        return self.env['calendar.event'].search(cond)
