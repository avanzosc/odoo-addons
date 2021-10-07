# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class EventEvent(models.Model):
    _inherit = "event.event"

    teacher_zoom = fields.Char(string="Teacher Zoom URL")
    student_zoom = fields.Char(string="Student Zoom URL")
    teacher_zoom_email = fields.Char(string="Email Address")
    teacher_zoom_pwd = fields.Char(string="Zoom Password")
    student_zoom_meetingid = fields.Char(string="Meeting ID")
    student_zoom_key = fields.Char(string="Key")
