# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class EventAttendanceReport(models.Model):
    _inherit = "event.attendance.report"

    claim_categ_id = fields.Many2one(
        string='Claim category', comodel_name='crm.claim.category',
        readonly="1")
    claim_id = fields.Many2one(
        string='Claim', comodel_name='crm.claim', readonly="1")

    def _select_event_attendace_report(self):
        select = super(
            EventAttendanceReport, self)._select_event_attendace_report()
        select = "{}, {}".format(
            select,
            "(case when r.student_id = claim.partner_id then claim.categ_id "
            "else null end) as claim_categ_id, "
            "(case when r.student_id = claim.partner_id then claim.id "
            "else null end) as claim_id")
        my_select = select.replace(
            "t.duration as real_hours,",
            "(case when r.student_id = claim.partner_id then 0 "
            "else t.duration end) as real_hours, ")
        return my_select

    def _from_event_attendace_report(self):
        super_from = super(
            EventAttendanceReport, self)._from_event_attendace_report()
        my_from = super_from.replace(
            "event_track t",
            "event_track t LEFT OUTER JOIN crm_claim claim on t.id = "
            "claim.event_track_id")
        return my_from
