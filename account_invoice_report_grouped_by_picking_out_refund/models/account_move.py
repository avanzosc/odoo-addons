# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from collections import OrderedDict

from odoo import models
from odoo.tools import float_is_zero


class AccountMove(models.Model):
    _inherit = "account.move"

    def lines_grouped_by_picking(self):
        """This prepares a data structure for printing the invoice report
        grouped by pickings."""
        self.ensure_one()
        picking_dict = OrderedDict()
        lines_dict = OrderedDict()
        picking_obj = self.env["stock.picking"]
        # Not change sign if the credit note has been created from reverse move option
        # and it has the same pickings related than the reversed invoice instead of sale
        # order invoicing process after picking reverse transfer
        sign = (
            -1.0
            if self.move_type == "out_refund"
            and (
                not self.reversed_entry_id
                or self.reversed_entry_id.picking_ids != self.picking_ids
            )
            else 1.0
        )
        # Let's get first a correspondance between pickings and sales order
        so_dict = {x.sale_id: x for x in self.picking_ids if x.sale_id}
        # Now group by picking by direct link or via same SO as picking's one
        previous_section = previous_note = False
        last_section_notes = []
        for line in self.invoice_line_ids.sorted(
            lambda ln: (-ln.sequence, ln.date, ln.move_name, -ln.id), reverse=True
        ):
            if line.display_type == "line_section":
                previous_section = line
                last_section_notes.append(
                    {
                        "picking": picking_obj,
                        "line": line,
                        "qty": 0.0,
                        "is_last_section_notes": True,
                    }
                )
                continue
            if line.display_type == "line_note":
                previous_note = line
                last_section_notes.append(
                    {
                        "picking": picking_obj,
                        "line": line,
                        "qty": 0.0,
                        "is_last_section_notes": True,
                    }
                )
                continue
            last_section_notes = []
            remaining_qty = line.quantity
            for move in line.move_line_ids:
                key = (move.picking_id, line)
                self._process_section_note_lines_grouped(
                    previous_section, previous_note, picking_dict, move.picking_id
                )
                picking_dict.setdefault(key, 0)
                qty = self._get_signed_quantity_done(line, move, sign)
                picking_dict[key] += qty
                remaining_qty -= qty
            if not line.move_line_ids and line.sale_line_ids:
                for so_line in line.sale_line_ids:
                    if so_dict.get(so_line.order_id):
                        key = (so_dict[so_line.order_id], line)
                        self._process_section_note_lines_grouped(
                            previous_section,
                            previous_note,
                            picking_dict,
                            so_dict[so_line.order_id],
                        )
                        picking_dict.setdefault(key, 0)
                        qty = so_line.product_uom_qty
                        picking_dict[key] += qty
                        remaining_qty -= qty
            elif not line.move_line_ids and not line.sale_line_ids:
                key = (picking_obj, line)
                self._process_section_note_lines_grouped(
                    previous_section, previous_note, lines_dict
                )
                picking_dict.setdefault(key, 0)
                qty = line.quantity
                picking_dict[key] += qty
                remaining_qty -= qty
            if not float_is_zero(
                remaining_qty,
                precision_rounding=line.product_id.uom_id.rounding or 0.01,
            ):
                self._process_section_note_lines_grouped(
                    previous_section, previous_note, lines_dict
                )
                lines_dict[line] = remaining_qty
        no_picking = [
            {"picking": picking_obj, "line": key, "quantity": value}
            for key, value in lines_dict.items()
        ]
        with_picking = [
            {"picking": key[0], "line": key[1], "quantity": value}
            for key, value in picking_dict.items()
        ]
        lines_to_sort = with_picking
        if last_section_notes:
            lines_to_sort += last_section_notes
        return no_picking + self._sort_grouped_lines(lines_to_sort)
