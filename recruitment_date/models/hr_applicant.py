# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    period_start_date = fields.Date(
        string='Period start date', tracking=True)
    period_end_date = fields.Date(
        string='Period end date', tracking=True)
