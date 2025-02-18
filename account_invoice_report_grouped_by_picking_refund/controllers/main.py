import ast
import re

from odoo import http
from odoo.http import request

from odoo.addons.web.controllers.main import ReportController


class ReportControllerInherit(ReportController):
    @http.route()
    def report_download(self, data, token, context=None):
        if "account.report_invoice_with_payments" not in data:
            return super().report_download(data, token, context)

        view = (
            request.env["ir.ui.view"]
            .sudo()
            .search(
                [
                    (
                        "key",
                        "=",
                        "account_invoice_report_grouped_by_picking.report_invoice_document",
                    )
                ],
                limit=1,
            )
        )

        data_list = ast.literal_eval(data)
        match = re.search(r"/(\d+)", data_list[0])
        if not match:
            return super().report_download(data, token, context)

        report_id = int(match.group(1))

        account_move = (
            request.env["account.move"].sudo().search([("id", "=", report_id)], limit=1)
        )

        if account_move and account_move.move_type in ("out_refund", "in_refund"):
            if view and view.active:
                view.write({"active": False})
                try:
                    result = super().report_download(data, token, context)
                finally:
                    view.write({"active": True})
                return result
            elif view:
                return super().report_download(data, token, context)

        return super().report_download(data, token, context)
