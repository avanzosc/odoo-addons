# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ResPartnerType(models.Model):
    _inherit = 'res.partner.type'

    analytic_account_id = fields.Many2one(
        string='Analytic Account', comodel_name='account.analytic.account',
        company_dependent=True, copy=False)
