# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ProjectTimeType(models.Model):
    _inherit = 'project.time.type'

    customer_billable = fields.Boolean(
        string='Billable to Customer', default=False)
    paid_employee = fields.Boolean(string='Is Paid to Employee', default=False)
