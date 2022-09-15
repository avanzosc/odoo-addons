# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    students_names = fields.Text(
        string='Students', compute="_compute_students_names", store=True)

    @api.depends("invoice_line_ids",
                 "invoice_line_ids.sale_order_line_id",
                 "invoice_line_ids.contract_line_id")
    def _compute_students_names(self):
        partner_obj = self.env['res.partner']
        for invoice in self.filtered(lambda x: x.move_type == "out_invoice"):
            students = partner_obj
            students_name = ""
            for line in invoice.invoice_line_ids.filtered(
                    lambda x: x.sale_order_line_id and x.contract_line_id):
                cond = [('sale_order_line_id', '=',
                         line.sale_order_line_id.id),
                        ('contract_line_id', '=', line.contract_line_id.id)]
                registration = self.env['event.registration'].search(
                    cond, limit=1)
                if registration and registration.student_id:
                    if registration.student_id not in students:
                        students += registration.student_id
            for line in invoice.invoice_line_ids.filtered(
                    lambda x: x.sale_order_line_id and not x.contract_line_id):
                sale_line = line.sale_order_line_id
                cond = [('event_id', '=', sale_line.event_id.id),
                        ('event_ticket_id', '=', sale_line.event_ticket_id.id),
                        ('sale_order_line_id', '=', sale_line.id)]
                registration = self.env['event.registration'].search(cond)
                if not registration:
                    sale = line.sale_order_line_id.order_id
                    my_line = sale.order_line.filtered(
                        lambda x: x.event_id.id == sale_line.event_id.id and
                        x.event_ticket_id)
                    if my_line and len(my_line) == 1:
                        cond = [('event_id', '=', my_line.event_id.id),
                                ('event_ticket_id', '=',
                                 my_line.event_ticket_id.id),
                                ('sale_order_line_id', '=', my_line.id)]
                        registration = self.env['event.registration'].search(
                            cond)
                if len(registration) == 1 and registration.student_id:
                    if registration.student_id not in students:
                        students += registration.student_id
                if len(registration) > 1:
                    for reg in registration.filtered(lambda x: x.student_id):
                        if reg.student_id not in students:
                            students += reg.student_id
            if students:
                cond = [("id", "in", students.ids)]
                final_students = partner_obj.search(
                    cond, order="name asc")
                for student in final_students:
                    students_name = (
                        student.name if not students_name else
                        "{}, {}".format(students_name, student.name))
            invoice.students_names = students_name
