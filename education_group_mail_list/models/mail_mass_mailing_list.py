# Copyright (c) 2019 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MailMassMailingList(models.Model):
    _inherit = 'mail.mass_mailing.list'

    group_id = fields.Many2one(
        string='Education group',
        comodel_name='education.group')
    academic_year_id = fields.Many2one(
        string='Academic year',
        comodel_name='education.academic_year',
        related='group_id.academic_year_id',
        store=True)
    company_id = fields.Many2one(
        string='Company',
        comodel_name='res.company',
        related="group_id.center_id.company_id",
        store=True)
    center_id = fields.Many2one(
        string='Center',
        comodel_name='res.partner',
        related="group_id.center_id",
        store=True)
    level_id = fields.Many2one(
        string='Level',
        comodel_name='education.level',
        related="group_id.level_id",
        store=True)
    course_id = fields.Many2one(
        string='Course',
        comodel_name='education.course',
        related="group_id.course_id",
        store=True)
    list_type = fields.Selection(
        selection=[('student', 'Student'),
                   ('progenitor', 'Progenitor'),
                   ('both', 'Both')],
        string='List type', default='both')
