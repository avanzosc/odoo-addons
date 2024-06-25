# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import SUPERUSER_ID, api


def stock_move_remove_literal(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        cond = [
            "|",
            ("name", "ilike", "Nuevo movimiento:%"),
            ("name", "ilike", "New Move:%"),
        ]
        moves = env["stock.move"].search(cond)
        for move in moves:
            name = False
            if "Nuevo movimiento:" in move.name:
                name = move.name.replace("Nuevo movimiento:", "")
            if "New Move:" in move.name:
                name = move.name.replace("New Move:", "")
            if name:
                move.name = name
    return
