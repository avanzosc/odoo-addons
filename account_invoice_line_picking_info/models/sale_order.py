# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_invoice_line(self, **optional_values):
        vals = super()._prepare_invoice_line(**optional_values)
        move_line_ids = [move_line[1] for move_line in vals["move_line_ids"]]
        move_lines = self.env["stock.move"].browse(move_line_ids)
        picking_names = move_lines._get_picking_names()
        vals["name"] = "%(pickings_name)s: %(name)s" % {
            "name": vals.get("name"),
            "pickings_name": picking_names,
        }
        return vals
