# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _put_pickings_in_line_name(self):
        pickings = self.env["stock.picking"]
        for move in self.move_line_ids:
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
        self.name = "%(num_picking)s: %(name)s" % {
            "name": self.name,
            "num_picking": num_picking,
        }
