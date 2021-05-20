# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    education_center_id = fields.Many2one(
        string='Education center', comodel_name='res.partner')
    education_center_phone = fields.Char(string='Education center phone', comodel_name='res.partner',
        related='education_center_id.phone')
