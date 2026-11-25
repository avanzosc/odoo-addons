# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def _pre_render_qweb_pdf(self, report_ref, res_ids=None, data=None):
        if (
            report_ref == "account.account_invoices"
            and "proforma" in data
            and data.get("proforma", False)
        ):
            data["proforma"] = False
        return super()._pre_render_qweb_pdf(report_ref, res_ids=res_ids, data=data)
