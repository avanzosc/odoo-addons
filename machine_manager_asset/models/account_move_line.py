# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _put_asset_in_machine(self):
        machine_obj = self.env["machine"]
        for line in self:
            for move in line.purchase_line_id.move_ids:
                for move_line in move.move_line_ids:
                    cond = [
                        ("account_asset_id", "=", False),
                        ("move_line_id", "=", move_line.id),
                    ]
                    if move_line.lot_id:
                        cond.append(("serial_id", "=", move_line.lot_id.id))
                    machine = machine_obj.search(cond, limit=1)
                    if machine:
                        machine.account_asset_id = line.asset_id.id
                        break
