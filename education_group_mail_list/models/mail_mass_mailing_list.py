# Copyright (c) 2019 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MailMassMailingList(models.Model):
    _inherit='mail.mass_mailing.list'

    group_id = fields.Many2one(
        string='Education group',
        comodel_name='education.group',
        required=True)
    academic_year_id = fields.Many2one(
        string='Academic year',
        comodel_name='education.academic_year',
        related='group_id.academic_year_id')
    company_id = fields.Many2one(
        string='Company',
        comodel_name='res.company',
        related="group_id.center_id.company_id")
    center_id = fields.Many2one(
        string='Center',
        comodel_name='res.partner',
        related="group_id.center_id")
    list_type = fields.Selection(selection=[
        ('student', 'Student'),
        ('progenitor', 'Progenitor'),
        ('both', 'Both')],
        string='List type', default='student'
    )
    