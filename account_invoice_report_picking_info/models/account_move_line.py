# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _get_picking_no_grouped(self):
        name = ""
        pickings = False
        if self.move_line_ids:
            pickings = self.mapped("move_line_ids.picking_id")
            for picking in pickings:
                name = picking.name if not name else "{}, {}".format(name, picking.name)
        if pickings and len(pickings) == 1:
            name = _("Picking: {}").format(name)
        if pickings and len(pickings) > 1:
            name = _("Pickings: {}").format(name)
        return name
