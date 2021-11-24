# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    contact_type_id = fields.Many2one(
        string='Contact type', comodel_name='res.partner.type',
        related='partner_id.contact_type_id', store=True)
