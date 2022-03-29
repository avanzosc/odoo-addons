# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    education_center_id = fields.Many2one(
        string='Education center', comodel_name='res.partner', store=True,
        related='partner_id.education_center_id')
