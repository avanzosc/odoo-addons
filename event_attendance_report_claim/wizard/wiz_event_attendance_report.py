# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class WizEventAttendanceReport(models.TransientModel):
    _inherit = "wiz.event.attendance.report"

    allowed_claim_categ_ids = fields.Many2many(
        string="Allowed claim categories",
        comodel_name="crm.claim.category",
        relation="rel_wiz_event_attendance_report_claim_categ",
        column1="wiz_id",
        column2="allowed_claim_categ_id",
    )
    allowed_claim_ids = fields.Many2many(
        string="Allowed claims",
        comodel_name="crm.claim",
        relation="rel_wiz_event_attendance_report_claim",
        column1="wiz_id",
        column2="allowed_claim_id",
    )
    claim_categ_id = fields.Many2one(
        string="Claim category", comodel_name="crm.claim.category"
    )
    claim_id = fields.Many2one(string="Claim", comodel_name="crm.claim")

    @api.onchange("claim_categ_id")
    def _onchange_claim_id(self):
        self.put_allowed_data()

    @api.onchange("claim_categ_id")
    def _onchange_claim_categ_id(self):
        self.put_allowed_data()

    def set_allowed_data(self):
        lines = super(WizEventAttendanceReport, self).set_allowed_data()
        claim_categories = lines.mapped("claim_categ_id")
        claims = lines.mapped("claim_id")
        self.allowed_claim_categ_ids = [(6, 0, claim_categories.ids)]
        self.allowed_claim_ids = [(6, 0, claims.ids)]
        return lines

    def filter_lines(self, lines):
        lines = super(WizEventAttendanceReport, self).filter_lines(lines)
        if self.claim_categ_id:
            lines = lines.filtered(
                lambda x: x.claim_categ_id.id == self.claim_categ_id.id
            )
        if self.claim_id:
            lines = lines.filtered(lambda x: x.claim_id.id == self.claim_id.id)
        return lines

    def count_num_filters(self, cont):
        cont = super(WizEventAttendanceReport, self).count_num_filters(cont)
        if self.claim_categ_id:
            cont += 1
        if self.claim_id:
            cont += 1
        return cont
