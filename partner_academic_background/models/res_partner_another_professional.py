# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ResPartnerAnotherProfessional(models.Model):
    _name = 'res.partner.another.professional'
    _description = 'Another professional'

    academic_background_id = fields.Many2one(
        string='Academic background',
        comodel_name='res.partner.academic.background')
    role = fields.Char(string='Role', required=True)
    professional_id = fields.Many2one(
        string='Professional', comodel_name='res.partner', store=True)
    phone = fields.Char(
        string='Phone', comodel_name='res.partner',
        related='professional_id.phone', store=True)
