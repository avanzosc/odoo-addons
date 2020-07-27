# Copyright 2020 Adrian Revilla - Avanzosc S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class MailTemplate(models.Model):
    _inherit = 'mail.template'

    company_id = fields.Many2one(string='Company',
                                 comodel_name='res.company')
