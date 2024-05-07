# Copyright 2023 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from collections import OrderedDict

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def lines_grouped_by_picking(self):
        self.ensure_one()
        result = super().lines_grouped_by_picking()
        picking_dict = OrderedDict()
        so_dict = {x.sale_id: x for x in self.picking_ids if x.sale_id}
        for line in self.invoice_line_ids.filtered(lambda x: not x.display_type):
            remaining_qty = line.quantity
            if not line.move_line_ids and line.sale_line_ids:
                for so_line in line.sale_line_ids:
                    if not so_dict.get(so_line.order_id):
                        key = (self.env["stock.picking"], line)
                        picking_dict.setdefault(key, 0)
                        qty = line.quantity
                        picking_dict[key] += qty
                        remaining_qty -= qty
        with_picking = [
            {"picking": key[0], "line": key[1], "quantity": value}
            for key, value in picking_dict.items()
        ]
        new_result = []
        for picking in with_picking:
            if picking.get("picking") == self.env["stock.picking"]:
                found = False
                for r in result:
                    if not r.get("picking") and r.get("line") == picking.get("line"):
                        found = True
                        break
                if not found:
                    new_result.append(
                        {
                            "picking": False,
                            "line": picking.get("line"),
                            "quantity": picking.get("quantity"),
                        }
                    )
        for r in result:
            new_result.append(
                {
                    "picking": r.get("picking"),
                    "line": r.get("line"),
                    "quantity": r.get("quantity"),
                }
            )
        return new_result
