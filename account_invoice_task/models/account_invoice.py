# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.model
    def invoice_line_move_line_get(self):
        line_obj = self.env["account.invoice.line"]
        iml_list = super(AccountInvoice, self).invoice_line_move_line_get()
        for iml_dict in iml_list:
            if iml_dict.get("invl_id", False):
                invoice_line = line_obj.browse(iml_dict.get("invl_id"))
                iml_dict["task_id"] = invoice_line.task_id.id
        return iml_list
