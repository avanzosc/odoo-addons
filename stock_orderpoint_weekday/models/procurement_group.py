# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProcurementGroup(models.Model):
    _inherit = "procurement.group"

    @api.model
    def run_scheduler(self, use_new_cursor=False, company_id=False):
        return super(
            ProcurementGroup, self.with_context(update_date=True)
        ).run_scheduler(use_new_cursor=use_new_cursor, company_id=company_id)
