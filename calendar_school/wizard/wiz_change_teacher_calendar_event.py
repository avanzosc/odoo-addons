# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class WizChangeTeacherCalendarEvent(models.TransientModel):
    _name = "wiz.change.teacher.calendar.event"
    _description = "Wizard for change teacher in meetings"

    from_date = fields.Date(string='Substitute teacher from')
    to_date = fields.Date(string='Substitute teacher until')
    substitute_teacher_id = fields.Many2one(
        string='Teacher making the substitution', comodel_name='hr.employee')
    lines_ids = fields.One2many(
        string='Teachers/Students to change', inverse_name='wiz_id',
        comodel_name='wiz.change.teacher.calendar.event.line')

    @api.onchange('from_date', 'to_date')
    def onchange_dates(self):
        if self.from_date and self.to_date:
            self.lines_ids = self._catch_lines_info()

    def _catch_lines_info(self):
        data = []
        superviseds = self.env['hr.employee.supervised.year'].browse(
            self.env.context.get('active_ids', []))
        from_date = '{} 00:00:00'.format(self.from_date)
        to_date = '{} 23:59:59'.format(self.to_date)
        students = superviseds.mapped('student_id')
        cond = [('supervised_year_id', '!=', False),
                ('teacher_id', '!=', False),
                ('start', '>=', from_date),
                ('start', '<=', to_date),
                ('student_id', 'in', students.ids)]
        calendars = self.env['calendar.event'].search(cond)
        my_list = {}
        for calendar in calendars:
            new_key = '{}-{}-{}'.format(
                calendar.supervised_year_id.school_year_id.id,
                calendar.teacher_id.id, calendar.student_id.id)
            if new_key not in my_list:
                my_list[new_key] = {
                    'tutor_per_year_id': calendar.supervised_year_id,
                    'year_id': calendar.supervised_year_id.school_year_id,
                    'teacher_id': calendar.teacher_id,
                    'student_id': calendar.student_id}
        for key in my_list.keys():
            data.append(
                (0, 0, {'tutor_per_year_id':
                        my_list.get(key).get('tutor_per_year_id').id,
                        'school_year_id': my_list.get(key).get('year_id').id,
                        'teacher_id': my_list.get(key).get('teacher_id').id,
                        'student_id': my_list.get(key).get('student_id').id
                        }))
        return data

    @api.multi
    def change_teacher(self):
        supervised_year_obj = self.env['hr.employee.supervised.year']
        superviseds = supervised_year_obj.browse(
            self.env.context.get('active_ids', []))
        from_date = '{} 00:00:00'.format(self.from_date)
        to_date = '{} 23:59:59'.format(self.to_date)
        for supervised in superviseds:
            for line in self.lines_ids:
                if (supervised.teacher_id != line.teacher_id or
                        supervised.student_id != line.student_id):
                    continue
                cond = [('school_year_id', '=', line.school_year_id.id),
                        ('teacher_id', '=', self.substitute_teacher_id.id),
                        ('student_id', '=', line.student_id.id)]
                new_teacher_supervised_year = supervised_year_obj.search(
                    cond, limit=1)
                if not new_teacher_supervised_year:
                    message = _(u"No Tutor per year found for new teacher {},"
                                " student {}, and school year {}.").format(
                        self.substitute_teacher_id.name, line.student_id.name,
                        line.school_year_id.name)
                    raise ValidationError(message)
                cond = [('teacher_id', '=', line.teacher_id.id),
                        ('start', '>=', from_date),
                        ('start', '<=', to_date),
                        ('student_id', '=', line.student_id.id)]
                calendars = self.env['calendar.event'].search(cond)
                if calendars:
                    calendars.write(
                        {'supervised_year_id': new_teacher_supervised_year.id,
                         'teacher_id': self.substitute_teacher_id.id})
                    supervised.write(
                        {'from_date': self.from_date,
                         'to_date': self.to_date,
                         'substitute_teacher_id':
                         self.substitute_teacher_id.id})
        return {'type': 'ir.actions.act_window_close'}


class WizChangeTeacherCalendarEventLine(models.TransientModel):
    _name = "wiz.change.teacher.calendar.event.line"
    _description = "Lines of wizard for change teacher in meetings"

    wiz_id = fields.Many2one(
        string='Wizard', comodel_name='wiz.change.teacher.calendar.event')
    tutor_per_year_id = fields.Many2one(
        string='Tutor per year', comodel_name='hr.employee.supervised.year')
    school_year_id = fields.Many2one(
        string='School year', comodel_name='education.academic_year',
        required=True)
    teacher_id = fields.Many2one(
        string='Teacher', comodel_name='hr.employee',
        required=True)
    student_id = fields.Many2one(
        string='Student', comodel_name='res.partner',
        required=True)
