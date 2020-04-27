# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


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
        year_obj = self.env['hr.employee.supervised.year']
        data = []
        superviseds = year_obj.browse(
            self.env.context.get('active_ids', []))
        from_date = '{} 00:00:00'.format(self.from_date)
        to_date = '{} 23:59:59'.format(self.to_date)
        students = superviseds.mapped('student_id')
        cond = [('supervised_year_id', 'in', superviseds.ids),
                ('teacher_id', '!=', False),
                ('start', '>=', from_date),
                ('start', '<=', to_date),
                ('student_id', 'in', students.ids)]
        calendars = self.env['calendar.event'].search(cond)
        years = calendars.mapped('supervised_year_id')
        treated = {}
        for year in years:
            if year not in treated:
                treated[year] = year
                data.append(
                    (0, 0, {'tutor_per_year_id': year.id,
                            'teacher_id': year.teacher_id.id,
                            'student_id': year.student_id.id
                            }))
        return data

    @api.multi
    def change_teacher(self):
        for line in self.lines_ids:
            vals = {'supervised_year_id': line.tutor_per_year_id.id,
                    'from_date': self.from_date,
                    'to_date': self.to_date,
                    'substitute_teacher_id': self.substitute_teacher_id.id}
            self.env['hr.employee.supervised.year.substitution'].create(vals)
        return {'type': 'ir.actions.act_window_close'}


class WizChangeTeacherCalendarEventLine(models.TransientModel):
    _name = "wiz.change.teacher.calendar.event.line"
    _description = "Lines of wizard for change teacher in meetings"

    wiz_id = fields.Many2one(
        string='Wizard', comodel_name='wiz.change.teacher.calendar.event')
    tutor_per_year_id = fields.Many2one(
        string='Supervised', comodel_name='hr.employee.supervised.year')
    teacher_id = fields.Many2one(
        string='Teacher', comodel_name='hr.employee',
        required=True)
    student_id = fields.Many2one(
        string='Student', comodel_name='res.partner',
        required=True)
