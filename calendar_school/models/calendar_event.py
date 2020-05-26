# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    supervised_year_id = fields.Many2one(
        comodel_name='hr.employee.supervised.year', string='Supervised')
    teacher_id = fields.Many2one(
        comodel_name='hr.employee', string='Teacher')
    student_id = fields.Many2one(
        comodel_name='res.partner', string='Student',
        domain=[('educational_category', '=', 'student')])
    family_id = fields.Many2one(
        comodel_name='res.partner', string='Family',
        domain=[('educational_category', '=', 'family')])
    state = fields.Selection(selection_add=[('done', 'Done'),
                                            ('cancel', 'Cancelled')])
    agenda = fields.Text(string='Agenda')
    center_id = fields.Many2one(
        string='Center', comodel_name='res.partner')

    @api.multi
    def action_open(self):
        self.write({
            'state': 'open',
        })

    @api.multi
    def action_done(self):
        if not all(self.mapped('description')):
            raise ValidationError(
                _('You must enter the description'))
        self.write({
            'state': 'done',
        })

    @api.multi
    def action_cancel(self):
        self.write({
            'state': 'cancel',
        })

    @api.multi
    def action_draft(self):
        self.write({
            'state': 'draft',
        })
