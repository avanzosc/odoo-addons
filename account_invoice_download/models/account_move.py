# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_invoice_pdf_proforma(self):
        result = super()._get_invoice_pdf_proforma()
        if "filename" in result and "_proforma" in result.get("filename"):
            result["filename"] = result.get("filename").replace("_proforma", "")
        return result
