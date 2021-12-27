# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    print_students = fields.Boolean(
        string='Print students',
        related='partner_id.invoice_report_print_students')
    students_name = fields.Char(
        string='Students name', compute='_compute_students_name')

    def _compute_students_name(self):
        for invoice in self:
            students_name = ""
            if (invoice.event_id and invoice.start_date_period and
                    invoice.end_date_period):
                registrations = invoice.event_id.registration_ids.filtered(
                    lambda x: x.student_id and x.real_date_start and
                    invoice.start_date_period >= x.real_date_start and
                    (not x.real_date_end or
                     (x.real_date_end and invoice.end_date_period <=
                      x.real_date_end)))
                for reg in registrations.filtered(lambda x: x.student_id):
                    students_name = (
                        reg.student_id.name if not students_name else
                        "{}; {}".format(students_name, reg.student_id.name))
            invoice.students_name = students_name
