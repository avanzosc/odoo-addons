# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        result = super().action_post()
        for move in self.filtered(
            lambda x: x.state == "posted" and x.move_type == "in_invoice"
        ):
            for found_line in move.invoice_line_ids.filtered(
                lambda z: z.display_type == "product"
            ):
                vals = found_line.product_id._assign_values_last_invoice_info(
                    found_line
                )
                found_line.product_id._update_invoice_supplier_last_info(vals)
        return result

    def button_cancel(self):
        result = super().button_cancel()
        for move in self.filtered(
            lambda x: x.state == "cancel" and x.move_type == "in_invoice"
        ):
            for line in move.invoice_line_ids.filtered(
                lambda z: z.display_type == "product"
            ):
                found_line = line.product_id._found_invoice_supplier_last_line()
                vals = line.product_id._assign_values_last_invoice_info(found_line)
                line.product_id._update_invoice_supplier_last_info(vals)
        return result

    def button_draft(self):
        result = super().button_draft()
        for move in self.filtered(
            lambda x: x.state == "draft" and x.move_type == "in_invoice"
        ):
            for line in move.invoice_line_ids.filtered(
                lambda z: z.display_type == "product"
            ):
                found_line = line.product_id._found_invoice_supplier_last_line()
                vals = line.product_id._assign_values_last_invoice_info(found_line)
                line.product_id._update_invoice_supplier_last_info(vals)
        return result
