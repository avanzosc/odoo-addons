# Copyright 2023-2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def lines_grouped_by_picking(self):
        self.ensure_one()
        result = super().lines_grouped_by_picking()
        extra_lines = []
        without_picking_line_ids = {
            line["line"].id
            for line in result
            if not line.get("picking") and line.get("line")
        }
        so_dict = {x.sale_id: x for x in self.picking_ids if x.sale_id}
        for line in self.invoice_line_ids.filtered(
            lambda ln: not ln.display_type and not ln.move_line_ids and ln.sale_line_ids
        ):
            if line.id in without_picking_line_ids:
                continue
            if not any(so_dict.get(so_line.order_id) for so_line in line.sale_line_ids):
                extra_lines.append(
                    {
                        "picking": False,
                        "line": line,
                        "quantity": line.quantity,
                    },
                )
        return extra_lines + result
