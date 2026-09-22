# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def check_sequence_notes_in_purchase(self):
        section_sale_line = self.find_line_section()
        notes_sale_line = self.find_line_notes()
        for purchase_line in self.purchase_line_ids:
            purchase_order = purchase_line.order_id
            if section_sale_line:
                purchase_order.find_sale_line_sequence_in_purchase_order(
                    section_sale_line
                )
            if notes_sale_line:
                purchase_order.find_sale_line_sequence_in_purchase_order(
                    notes_sale_line
                )

    def find_line_section(self):
        sequence = self.sequence
        section_sale_line = self.env["sale.order.line"]
        lines = self.order_id.order_line.filtered(lambda x: x.sequence < sequence)
        if lines:
            lines = sorted(lines, key=lambda r: r.sequence, reverse=True)
            for line in lines:
                if line.display_type == "line_section":
                    section_sale_line = line
                    break
        return section_sale_line

    def find_line_notes(self):
        sequence = self.sequence
        notes_sale_line = self.env["sale.order.line"]
        lines = self.order_id.order_line.filtered(lambda x: x.sequence > sequence)
        if lines:
            lines = sorted(lines, key=lambda r: r.sequence)
            for line in lines:
                if line.display_type == "line_note":
                    notes_sale_line = line
                    break
        return notes_sale_line

    def write(self, values):
        result = super().write(values)
        if "sequence" in values:
            for line in self:
                if line.purchase_line_ids:
                    line.purchase_line_ids.write({"sequence": values.get("sequence")})
        return result
