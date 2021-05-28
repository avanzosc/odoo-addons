# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class HrJob(models.Model):
    _inherit = 'hr.job'

    validity_start_date = fields.Date(
        string='Validity start date', tracking=True)
    validity_end_date = fields.Date(
        string='Validity end date', tracking=True)
    partner_id = fields.Many2one(
        string='Partner', comodel_name='res.partner')
