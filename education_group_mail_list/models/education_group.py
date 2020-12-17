# Copyright (c) 2019 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class EducationGroup(models.Model):
    _inherit = "education.group"

    mail_list_ids = fields.One2many(
        comodel_name="mail.mass_mailing.list", inverse_name="group_id",
        string="Mail Lists")
    mail_list_count = fields.Integer(
        compute="_compute_mail_list_count", string="# Mail List",
        compute_sudo=True, store=True)

    @api.depends("mail_list_ids")
    def _compute_mail_list_count(self):
        for group in self:
            group.mail_list_count = len(group.mail_list_ids)

    @api.multi
    def button_open_mail_list(self):
        action = self.env.ref("mass_mailing.action_view_mass_mailing_lists")
        action_dict = action.read()[0] if action else {}
        action_dict['context'] = safe_eval(
            action_dict.get('context', '{}'))
        if len(self) == 1:
            action_dict['context'].update({
                'search_default_group_id': self.id,
                'default_group_id': self.id,
            })
        domain = expression.AND([
            [('group_id', 'in', self.ids)],
            safe_eval(action.domain or '[]')])
        action_dict.update({'domain': domain})
        return action_dict

    @api.multi
    def generate_lists(self):
        mail_list_obj = self.env["mail.mass_mailing.list"]
        list_contact_obj = self.env["mail.mass_mailing.contact"]
        for group in self.filtered("student_ids"):
            list_name = "{}-{}-{}".format(
                group.academic_year_id.name,
                group.center_id.name,
                group.display_name)
            student_mail_list = mail_list_obj.search([
                ("group_id", "=", group.id),
                ("list_type", "=", "student")])
            if not student_mail_list:
                student_mail_list = mail_list_obj.create({
                    "group_id": group.id,
                    "name": _("{} - Students").format(list_name),
                    "list_type": "student",
                    "partner_mandatory": True,
                })
            for student in group.student_ids:
                if not student.email:
                    student.email = "{}@nomail.no".format(student.name)
                contact = list_contact_obj.find_or_create(student)
                contact.write({
                    "list_ids": [(4, student_mail_list.id)],
                })
            progenitor_mail_list = mail_list_obj.search([
                ("group_id", "=", group.id),
                ("list_type", "=", "progenitor")])
            if not progenitor_mail_list:
                progenitor_mail_list = mail_list_obj.create({
                    "group_id": group.id,
                    "name": _("{} - Progenitor").format(list_name),
                    "list_type": "progenitor",
                    "partner_mandatory": True,
                })
            for progenitor in group.mapped(
                    "student_ids.student_progenitor_ids"):
                if not progenitor.email:
                    progenitor.email = "{}@nomail.no".format(
                        progenitor.name)
                contact = list_contact_obj.find_or_create(progenitor)
                contact.write({
                    "list_ids": [(4, progenitor_mail_list.id)],
                })
        return self.button_open_mail_list()
