# Copyright 2022 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    registration_ids = fields.One2many(
        string="Event registrations", comodel_name="event.registration",
        inverse_name="sale_order_id")
    students_names = fields.Text(
        string='Students', compute="_compute_students_names", store=True)

    @api.depends("registration_ids", "registration_ids.state",
                 "registration_ids.student_id")
    def _compute_students_names(self):
        partner_obj = self.env['res.partner']
        for sale in self:
            students = partner_obj
            students_name = ""
            for registration in sale.registration_ids.filtered(
                    lambda x: x.state != "cancel"):
                if (registration.student_id and
                        registration.student_id not in students):
                    students += registration.student_id
            if students:
                cond = [("id", "in", students.ids)]
                final_students = partner_obj.search(
                    cond, order="name asc")
                for student in final_students:
                    students_name = (
                        student.name if not students_name else
                        "{}, {}".format(students_name, student.name))
            sale.students_names = students_name
