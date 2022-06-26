# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class EventAttendanceReport(models.Model):
    _inherit = "event.attendance.report"

    payable = fields.Float(
        string="Payable", readonly="1")
    billable = fields.Float(
        string="Billable", readonly="1")

    def _select_event_attendace_report(self):
        select = super(
            EventAttendanceReport, self)._select_event_attendace_report()
        return "{}, {}".format(
            select, "t.payable as payable, t.billable as billable")
