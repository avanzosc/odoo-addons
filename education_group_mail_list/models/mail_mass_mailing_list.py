# Copyright 2019 Adrian Revilla - AvanzOSCcenter_id
# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.models import expression
import logging

logger = logging.getLogger(__name__)


class MailMassMailingList(models.Model):
    _inherit = 'mail.mass_mailing.list'

    group_id = fields.Many2one(
        string='Education Group',
        comodel_name='education.group')
    academic_year_id = fields.Many2one(
        string='Academic Year',
        comodel_name='education.academic_year')
    center_id = fields.Many2one(
        string='Education Center',
        comodel_name='res.partner')
    company_id = fields.Many2one(
        string='Company',
        comodel_name='res.company',
        related="center_id.company_id",
        store=True)
    level_id = fields.Many2one(
        string='Education Level',
        comodel_name='education.level')
    course_id = fields.Many2one(
        string='Education Course',
        comodel_name='education.course')
    list_type = fields.Selection(
        selection=[('student', 'Student'),
                   ('progenitor', 'Progenitor'),
                   ('both', 'Both')],
        string='List Type', default='both')
    groups_sync_domain = fields.Many2many(
        comodel_name="education.group",
        string="Groups",
        compute="_compute_groups_sync_domain",
        relation="rel_education_group_mail_list",
        column1="mail_list_id",
        column2="edu_group_id")

    @api.depends(
        "academic_year_id", "center_id", "level_id", "course_id", "group_id")
    def _compute_groups_sync_domain(self):
        group_obj = self.env["education.group"]
        for record in self:
            groups = record.group_id
            if not record.group_id:
                group_domain = [("group_type_id.type", "=", "official")]
                if record.academic_year_id:
                    group_domain = expression.AND(
                        [[("academic_year_id", "=",
                           record.academic_year_id.id)],
                         group_domain])
                if record.center_id:
                    group_domain = expression.AND(
                        [[("center_id", "=", record.center_id.id)],
                         group_domain])
                if record.level_id:
                    group_domain = expression.AND(
                        [[("level_id", "=", record.level_id.id)],
                         group_domain])
                if record.course_id:
                    group_domain = expression.AND(
                        [[("course_id", "=", record.course_id.id)],
                         group_domain])
                groups = group_obj.search(group_domain)
            record.groups_sync_domain = [(6, 0, groups.ids)]

    @api.onchange("group_id")
    def _onchange_group_id(self):
        self.academic_year_id = self.group_id.academic_year_id
        self.center_id = self.group_id.center_id
        self.level_id = self.group_id.level_id
        self.course_id = self.group_id.course_id

    @api.multi
    def button_update_domain(self):
        for record in self.filtered(lambda l: l.dynamic):
            student_domain = [
                ("student_group_ids", "in", record.groups_sync_domain.ids)]
            progenitor_domain = [
                ("progenitor_child_ids.student_group_ids", "in",
                 record.groups_sync_domain.ids)]
            if record.list_type == "student":
                record.sync_domain = student_domain
            elif record.list_type == "progenitor":
                record.sync_domain = progenitor_domain
            else:
                record.sync_domain = expression.OR([
                    student_domain, progenitor_domain])

    @api.model
    def _mailing_list_automatic_sync(self):
        logger.info('Searching for Mail List that must be synced')
        mailing_lists = self.search(
            [('dynamic', '=', True),
             '|',
             ('academic_year_id.end_date', '>=',
              fields.Date.context_today(self)),
             ('academic_year_id', '=', False)])
        if mailing_lists:
            mailing_lists.button_update_domain()
            mailing_lists.action_sync()
            logger.info(
                'The following Mail List IDs have been synced: %s'
                % mailing_lists.ids)
        else:
            logger.info('0 Mail List had to be synced')
        return True
