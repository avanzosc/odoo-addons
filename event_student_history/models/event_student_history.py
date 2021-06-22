# Copyright 2021 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class EventStudentHistory(models.Model):
    _name = 'event.student.history'
    _description = "Student's Event History"

    event_name = fields.Char(string='Event Name')
    event_type = fields.Char(string='Event Type')
    event_state = fields.Char(string='Event State')
    student_id = fields.Many2one(
        string='Student', comodel_name='res.partner')
    birthdate_date = fields.Date(
        related="student_id.birthdate_date", string="Birthdate")
    bank_acc_count = fields.Integer(
        related="student_id.mandate_count", string="Bank Acc Qty")
    mandate_count = fields.Integer(
        related="student_id.mandate_count", string="Mandate Qty")
    date_begin = fields.Datetime(string='Start Date')
    date_end = fields.Datetime(string='End Date')
