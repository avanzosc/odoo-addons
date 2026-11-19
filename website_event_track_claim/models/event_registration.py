# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    student_id = fields.Many2one(string="Student", comodel_name="res.partner")

    @api.onchange("student_id", "partner_id")
    def _onchange_student_id(self):
        if self.student_id:
            self.name = self.student_id.name
            self.email = (
                self.student_id.email
                if self.student_id.email
                else self.partner_id.email
            )
            self.phone = (
                self.student_id.phone
                if self.student_id.phone
                else self.partner_id.phone
            )
        if not self.student_id and self.partner_id:
            if not self.name:
                self.name = self.partner_id.name
            if not self.email:
                self.email = self.partner_id.email
            if not self.phone:
                self.phone = self.partner_id.phone
