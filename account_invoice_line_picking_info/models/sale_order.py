# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_invoice_line(self, **optional_values):
        vals = super()._prepare_invoice_line(**optional_values)
        moves = self.get_stock_moves_link_invoice()
        if moves:
            pickings = self.env["stock.picking"]
            for move in moves:
                if move.picking_id not in pickings:
                    pickings += move.picking_id
            num_pickings = ""
            for picking in pickings:
                if not num_pickings:
                    num_picking = picking.name
                else:
                    num_picking = "%(num_picking)s, %(picking_name)s" % {
                        "num_picking": num_picking,
                        "picking_name": picking.name,
                    }
            vals["name"] = "%(num_picking)s: %(name)s" % {
                "name": vals.get("name"),
                "num_picking": num_picking,
            }
        return vals
