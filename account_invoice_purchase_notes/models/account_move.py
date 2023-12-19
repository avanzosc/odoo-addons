# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, models


class AccountMove(models.Model):
    _inherit = "account.move"

    def put_notes_from_purchase_order(self):
        lines = self.invoice_line_ids.filtered(
            lambda x: not x.display_type and x.purchase_order_id)
        purchase_orders = lines.mapped("purchase_order_id")
        for purchase_order in purchase_orders:
            note_lines = purchase_order.order_line.filtered(
                lambda x: x.display_type == "line_note")
            for note_line in note_lines:
                line = self.invoice_line_ids.filtered(
                    lambda x: x.purchase_line_id == note_line.id)
                if not line:
                    self.continue_put_notes_from_purchase_order(
                        purchase_order, note_line)

    def continue_put_notes_from_purchase_order(self, purchase, note_line):
        previous_line = self.env["purchase.order.line"]
        posterior_line = self.env["purchase.order.line"]
        found = False
        for line in purchase.order_line:
            if not found and line.id != note_line.id:
                previous_line = line
            if line.id == note_line.id:
                found = True
            if line.id != note_line.id and found and not posterior_line:
                posterior_line = line
        if previous_line and previous_line.id == note_line.id:
            previous_line = self.env["purchase.order.line"]
        if found:
            purchase_line = previous_line if previous_line else posterior_line
            if purchase_line:
                invoice_line = self.invoice_line_ids.filtered(
                    lambda x: x.purchase_line_id.id == purchase_line.id)
                sequence = 0
                if invoice_line:
                    if previous_line:
                        sequence = invoice_line.sequence + 5
                    else:
                        if posterior_line:
                            sequence = invoice_line.sequence - 5
                    name = _(u"{}: {}").format(note_line.order_id.name,
                                               note_line.name)
                    vals = {"name": name,
                            "move_id": self.id,
                            "sequence": sequence,
                            "display_type": "line_note",
                            "purchase_line_id": note_line.id,
                            "exclude_from_invoice_tab": False}
                    self.env["account.move.line"].create(vals)
