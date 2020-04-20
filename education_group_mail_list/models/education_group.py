# Copyright (c) 2019 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class EducationGroup(models.Model):
    _inherit='education.group'
    
    @api.multi
    def generate_lists(self):
        mail_list_ids = self.env['mail.mass_mailing.list']
        for group in self:
            group_mail_list_ids = mail_list_ids.search([('group_id', '=', group.id)])
            if not group_mail_list_ids:
                student_mail_list_id = mail_list_ids.create({
                    'group_id': group.id,
                    'name': group.academic_year_id.name + " " + group.center_id.company_id.name + " " + group.center_id.name + " " + group.display_name + " - Students",
                    'list_type': 'student'
                    })
                progenitor_mail_list_id = mail_list_ids.create({
                    'group_id': group.id,
                    'name': group.academic_year_id.name + " " + group.center_id.company_id.name + " " + group.center_id.name + " " + group.display_name + " - Progenitor / Tutor",
                    'list_type': 'progenitor'
                    })
                for student in group.student_ids:
                    if not student.email:
                        email = str(student.name) + "@nomail.no"
                    else:
                        email = student.email
                    mailing_contact_id = self.env['mail.mass_mailing.contact'].create({
                        'email': email,
                        'company_name':student.company_id.name,
                        'name': student.name
                        })
                    self.env['mail.mass_mailing.list_contact_rel'].create({
                        'contact_id': mailing_contact_id.id,
                        'list_id': student_mail_list_id.id
                        })
                for teacher in group.teacher_ids:
                    if not teacher.employee_id.work_email:
                        email = str(teacher.employee_id.name) + "@nomail.no"
                    else:
                        email = teacher.employee_id.work_email
                    mailing_contact_id = self.env['mail.mass_mailing.contact'].create({
                        'email': email,
                        'company_name':teacher.employee_id.company_id.name,
                        'name': teacher.employee_id.name
                        })
                    self.env['mail.mass_mailing.list_contact_rel'].create({
                        'contact_id': mailing_contact_id.id,
                        'list_id': progenitor_mail_list_id.id
                        })
    