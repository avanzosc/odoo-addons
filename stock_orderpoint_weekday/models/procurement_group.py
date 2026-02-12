# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProcurementGroup(models.Model):
    _inherit = "procurement.group"

    @api.model
    def run_scheduler(self, use_new_cursor=False, company_id=False):
        company = self.env["res.company"].browse(company_id) or self.env.company
        update_date = company.update_weekday_orderpoint if company else True
        return super(
            ProcurementGroup, self.with_context(update_date=update_date)
        ).run_scheduler(use_new_cursor=use_new_cursor, company_id=company_id)
