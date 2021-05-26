# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class CrmPhonecall(models.Model):
    _inherit = 'crm.phonecall'

    academic_background_id = fields.Many2one(
        string='Academic background',
        comodel_name='res.partner.academic.background')
