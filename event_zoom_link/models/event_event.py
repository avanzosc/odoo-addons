# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class EventEvent(models.Model):
    _inherit = 'event.event'

    teacher_zoom = fields.Char(string='Teacher Zoom URL')
    student_zoom = fields.Char(string='Student Zoom URL')
    email_address = fields.Char(string='Email Address')
    password = fields.Char('Password')
    meeting_id = fields.Char(string='Meeting ID')
    key = fields.Char(string='Key')
