# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class EventTrack(models.Model):
    _inherit = "event.track"

    teacher_zoom = fields.Char(
        string="Teacher Zoom URL",
        related="event_id.teacher_zoom")
    student_zoom = fields.Char(
        string="Student Zoom URL",
        related="event_id.student_zoom")
    teacher_zoom_email = fields.Char(
        string="Email Address",
        related="event_id.teacher_zoom_email")
    teacher_zoom_pwd = fields.Char(
        string="Zoom Password",
        related="event_id.teacher_zoom_pwd")
    student_zoom_meetingid = fields.Char(
        string="Meeting ID",
        related="event_id.student_zoom_meetingid")
    student_zoom_key = fields.Char(
        string="Key",
        related="event_id.student_zoom_key")
