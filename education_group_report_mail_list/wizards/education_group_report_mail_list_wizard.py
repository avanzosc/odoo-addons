# Copyright (c) 2020 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class educationGroupStudentReportWizard(models.TransientModel):
    _name = "education.group.student.report.wizard"
    _description = "Wizard to add students and progenitors into mail list"

    mass_mailing_list_id = fields.Many2one(
        string="Mail list",
        comodel_name="mail.mass_mailing.list", required="True",
        domain="[('list_type', '=', 'student')]")
    group_id = fields.Many2one(
        string="Education group",
        related="mass_mailing_list_id.group_id",
        comodel_name="education.group",
        store=True)
    mass_mailing_list_id_2 = fields.Many2one(
        string="Progenitor mail list",
        comodel_name="mail.mass_mailing.list",
        domain="[('list_type', '=', 'progenitor')," +
        "('group_id', '=', group_id)]")

    @api.multi
    def button_update_list(self):
        self.ensure_one()
        partner_report_id = self.env[
            'education.group.student.report'].search(
                [('id', '=', self.env.context.get("active_id"))])
        if self.mass_mailing_list_id:
            self.addStudentToList(
                partner_report_id.student_id, self.mass_mailing_list_id)
        if self.mass_mailing_list_id_2:
            self.addProgenitorsToList(
                partner_report_id.student_id.student_progenitor_ids,
                self.mass_mailing_list_id_2)

    def addStudentToList(self, student_id, list_id):
        if not self.partnerExistInList(student_id, list_id):
            if not student_id.email:
                email = str(student_id.name) + "@nomail.no"
            else:
                email = student_id.email
            if not self.partnerExist(student_id):
                mailing_contact_id = self.env[
                    'mail.mass_mailing.contact'].create({
                        'email': email,
                        'company_name': student_id.company_id.name,
                        'name': student_id.name
                        })
            else:
                mailing_contact_id = self.env[
                    'mail.mass_mailing.contact'].search(
                        [('email', '=', email)])
            self.env['mail.mass_mailing.list_contact_rel'].create({
                'contact_id': mailing_contact_id.id,
                'list_id': list_id.id
            })

    def addProgenitorsToList(self, progenitor_ids, list_id):
        for progenitor in progenitor_ids:
            if not self.partnerExistInList(progenitor, list_id):
                if not progenitor.email:
                    email = str(progenitor.name) + "@nomail.no"
                else:
                    email = progenitor.email
                if not self.partnerExist(progenitor):
                    mailing_contact_id = self.env[
                        'mail.mass_mailing.contact'].create({
                            'email': email,
                            'company_name': progenitor.company_id.name,
                            'name': progenitor.name
                            })
                else:
                    mailing_contact_id = self.env[
                        'mail.mass_mailing.contact'].search(
                            [('email', '=', email)])
                self.env['mail.mass_mailing.list_contact_rel'].create({
                    'contact_id': mailing_contact_id.id,
                    'list_id': list_id.id
                })

    def partnerExistInList(self, partner_id, list_id):
        list_contact_id = self.env[
            'mail.mass_mailing.list_contact_rel'].search_count([
                ('contact_id.email', 'in',
                 (partner_id.email, str(partner_id.name)+'@nomail.no')),
                ('list_id', '=', list_id.id)])
        return list_contact_id > 0

    def partnerExist(self, partner_id):
        list_contact_id = self.env[
            'mail.mass_mailing.contact'].search_count(
                [('email', 'in',
                  (partner_id.email, str(partner_id.name)+'@nomail.no'))])
        return list_contact_id > 0
