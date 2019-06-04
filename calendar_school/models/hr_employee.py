# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from pytz import timezone, utc

str2date = fields.Date.from_string
str2datetime = fields.Datetime.from_string
date2str = fields.Date.to_string


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    meetings_ids = fields.One2many(
        comodel_name='calendar.event',
        inverse_name='teacher_id', string='Tutoring meetings')
    count_meetings = fields.Integer(
        string='# Tutoring meetings', compute='_compute_count_meetings')

    def _compute_count_meetings(self):
        for employee in self:
            employee.count_meetings = (len(employee.meetings_ids))

    @api.multi
    def button_show_meetings(self):
        self.ensure_one()
        self = self.with_context(
            search_default_teacher_id=self.id, default_teacher_id=self.id)
        return {'name': _('Tutoring meetings'),
                'type': 'ir.actions.act_window',
                'view_mode': 'calendar,tree,form',
                'view_type': 'form',
                'res_model': 'calendar.event',
                'domain': [('id', 'in', self.meetings_ids.ids)],
                'context': self.env.context}


class hrEmployeeSupervisedYear(models.Model):
    _inherit = 'hr.employee.supervised.year'

    meeting_ids = fields.One2many(
        comodel_name='calendar.event', inverse_name='supervised_year_id',
        string='Meetings')
    count_meetings = fields.Integer(
        string='# Tutoring meetings', compute='_compute_count_meetings')

    def _compute_count_meetings(self):
        for year in self:
            year.count_meetings = (len(year.meeting_ids))

    @api.multi
    def button_show_meetings(self):
        self.ensure_one()
        self = self.with_context(
            search_default_supervised_year_id=self.id,
            default_supervised_year_id=self.id,
            search_default_teacher_id=self.teacher_id.id,
            default_teacher_id=self.teacher_id.id,
            search_default_student_id=self.student_id.id,
            default_student_id=self.student_id.id)
        return {'name': _('Tutoring meetings'),
                'type': 'ir.actions.act_window',
                'view_mode': 'calendar,tree,form',
                'view_type': 'form',
                'res_model': 'calendar.event',
                'domain': [('id', 'in', self.meeting_ids.ids)],
                'context': self.env.context}

    @api.multi
    def generate_meetings(self):
        for supervised in self:
            first_day = "{}-{}-01".format(
                int(str2date(supervised.school_year_id.date_start).year),
                str(int(str2date(
                    supervised.school_year_id.date_start).month)).zfill(2))
            first_day = str2date(first_day)
            while first_day <= str2date(supervised.school_year_id.date_end):
                month = self.env['base.month'].search(
                    [('number', '=', first_day.month)])
                cond = [('school_id', '=',
                         supervised.student_id.current_center_id.id),
                        ('course_id', '=',
                         supervised.student_id.current_course_id.id),
                        ('type', '=', 'student'),
                        ('month_id', '=', month.id),
                        ('meeting_day', '=', str(first_day.day))]
                agenda = self.env['education.order.day'].search(cond, limit=1)
                if (agenda and not
                        supervised._generate_event(first_day, False)):
                    supervised._create_calendar_event_for_student(
                        date2str(first_day))
                cond = [('school_id', '=',
                         supervised.student_id.current_center_id.id),
                        ('course_id', '=',
                         supervised.student_id.current_course_id.id),
                        ('type', '=', 'family'),
                        ('month_id', '=', month.id),
                        ('meeting_day', '=', str(first_day.day))]
                agenda = self.env['education.order.day'].search(cond, limit=1)
                if agenda:
                    families = set(supervised.student_id.mapped(
                        'child2_ids.family_id'))
                    for family in families:
                        lines = supervised.student_id.mapped(
                            'child2_ids').filtered(lambda c: c.family_id.id ==
                                                   family.id)
                        responsibles = set(lines.mapped('responsible_id'))
                        progenitors = self.env['res.partner']
                        for p in responsibles:
                            progenitors += p
                        if (progenitors and not
                                supervised._generate_event(first_day, family)):
                            supervised._create_calendar_event_for_progenitor(
                                date2str(first_day), family, progenitors)
                first_day += relativedelta(days=1)

    def _generate_event(self, day, family):
        start1 = "{} {}".format(date2str(day), '00:00:01')
        start2 = "{} {}".format(date2str(day), '23:59:59')
        cond = [('supervised_year_id', '=', self.id),
                ('teacher_id', '=', self.teacher_id.id),
                ('student_id', '=', self.student_id.id),
                ('start', '>=', start1),
                ('start', '<=', start2)]
        if family:
            cond.append(('family_id', '=', family.id))
        else:
            cond.append(('family_id', '=', False))
        return self.env['calendar.event'].search(cond, limit=1)

    def _create_calendar_event_for_student(self, day):
        vals = self._catch_values_for_student(day)
        self.env['calendar.event'].create(vals)

    def _catch_values_for_student(self, day):
        label = self.env.ref('calendar_school.calendar_event_type_student_'
                             'tutoring')
        alarm = self.env.ref('calendar.alarm_notif_1')
        start = self._convert_to_utc_date(
            "{} {}".format(day, '09:00:00'), tz=self.env.user.tz)
        stop = self._convert_to_utc_date(
            "{} {}".format(day, '09:15:00'), tz=self.env.user.tz)
        vals = {
            'name': _('Meeting'),
            'supervised_year_id': self.id,
            'allday': False,
            'start': start,
            'stop': stop,
            'duration': 0.25,
            'user_id': self.teacher_id.user_id.id,
            'alarm_ids': [(6, 0, [alarm.id])],
            'partner_ids': [(6, 0, [self.student_id.id,
                                    self.teacher_id.user_id.partner_id.id])],
            'categ_ids': [(6, 0, [label.id])]}
        if (self.student_id.current_center_id and
                self.student_id.current_course_id):
            day = str2date(day)
            month = self.env['base.month'].search([('number', '=', day.month)])
            cond = [('school_id', '=', self.student_id.current_center_id.id),
                    ('course_id', '=', self.student_id.current_course_id.id),
                    ('type', '=', 'student'),
                    ('month_id', '=', month.id),
                    ('meeting_day', '=', str(day.day))]
            agendas = self.env['education.order.day'].search(cond)
            if agendas:
                lit = ''
                for agenda in agendas:
                    lit += u"{}\n".format(agenda.order_day)
                vals['agenda'] = lit
        return vals

    def _create_calendar_event_for_progenitor(self, day, family, progenitors):
        vals = self._catch_values_for_progenitor(day, family, progenitors)
        self.env['calendar.event'].create(vals)

    def _catch_values_for_progenitor(self, day, family, progenitors):
        label = self.env.ref('calendar_school.calendar_event_type_family_'
                             'tutoring')
        alarm = self.env.ref('calendar.alarm_notif_1')
        start = self._convert_to_utc_date(
            "{} {}".format(day, '15:00:00'), tz=self.env.user.tz)
        stop = self._convert_to_utc_date(
            "{} {}".format(day, '15:30:00'), tz=self.env.user.tz)
        partners = self.teacher_id.user_id.partner_id.ids + progenitors.ids
        vals = {
            'name': _('Meeting'),
            'supervised_year_id': self.id,
            'allday': False,
            'start': start,
            'stop': stop,
            'duration': 0.50,
            'user_id': self.teacher_id.user_id.id,
            'family_id': family.id,
            'alarm_ids': [(6, 0, [alarm.id])],
            'partner_ids': [(6, 0, partners)],
            'categ_ids': [(6, 0, [label.id])]}
        if (self.student_id.current_center_id and
                self.student_id.current_course_id):
            day = str2date(day)
            month = self.env['base.month'].search([('number', '=', day.month)])
            cond = [('school_id', '=', self.student_id.current_center_id.id),
                    ('course_id', '=', self.student_id.current_course_id.id),
                    ('type', '=', 'family'),
                    ('month_id', '=', month.id),
                    ('meeting_day', '=', str(day.day))]
            agendas = self.env['education.order.day'].search(cond)
            if agendas:
                lit = ''
                for agenda in agendas:
                    lit += u"{}\n".format(agenda.order_day)
                vals['agenda'] = lit
        return vals

    def _convert_to_utc_date(self, date, tz=u'UTC'):
        if not date:
            return False
        if not tz:
            tz = u'UTC'
        date = str2datetime(date)
        local = timezone(tz)
        local_date = local.localize(date, is_dst=None)
        utc_date = local_date.astimezone(utc).replace(tzinfo=None)
        return utc_date
