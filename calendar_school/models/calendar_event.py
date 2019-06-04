# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, _
from odoo.exceptions import ValidationError


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    supervised_year_id = fields.Many2one(
        comodel_name='hr.employee.supervised.year', string='Supervised')
    teacher_id = fields.Many2one(
        comodel_name='hr.employee', string='Teacher',
        related='supervised_year_id.teacher_id', store=True)
    student_id = fields.Many2one(
        comodel_name='res.partner', string='Student',
        related='supervised_year_id.student_id', store=True)
    family_id = fields.Many2one(
        comodel_name='res.partner', string='Family',
        domain=[('educational_category', '=', 'family')])
    state = fields.Selection(
        selection=[('draft', 'Unrealized'),
                   ('open', 'Confirmed'),
                   ('done', 'Realized'),
                   ('cancel', 'Cancelled')])
    agenda = fields.Text(string='Agenda')

    def action_confirmed(self):
        self.state = 'open'

    def action_realized(self):
        if not self.description:
            raise ValidationError(
                _('You must enter the description'))
        self.state = 'done'

    def action_canceled(self):
        self.state = 'cancel'
