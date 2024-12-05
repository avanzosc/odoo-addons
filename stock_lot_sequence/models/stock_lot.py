# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class StockLot(models.Model):
    _inherit = "stock.lot"

    @api.model_create_multi
    def create(self, vals_list):
        if isinstance(vals_list, dict):
            lot = super().create(vals_list)
            if len(lot.name) == 5 and "9999" in lot.name:
                self.update_lot_sequence()
            return lot
        else:
            lots = self.env["stock.lot"]
            for vals in vals_list:
                lot = super().create(vals)
                lots += lot
                if len(lot.name) == 5 and "9999" in lot.name:
                    self.update_lot_sequence()
            return lots

    def update_lot_sequence(self):
        sequence = self.env.ref("stock.sequence_production_lots")
        prefix = False
        if sequence.prefix == "A":
            prefix = "B"
        if sequence.prefix == "B":
            prefix = "C"
        if sequence.prefix == "C":
            prefix = "D"
        if sequence.prefix == "D":
            prefix = "E"
        if sequence.prefix == "E":
            prefix = "F"
        if sequence.prefix == "F":
            prefix = "G"
        if sequence.prefix == "G":
            prefix = "H"
        if sequence.prefix == "H":
            prefix = "I"
        if sequence.prefix == "I":
            prefix = "J"
        if sequence.prefix == "J":
            prefix = "K"
        if sequence.prefix == "K":
            prefix = "L"
        if sequence.prefix == "L":
            prefix = "M"
        if sequence.prefix == "M":
            prefix = "N"
        if sequence.prefix == "N":
            prefix = "Ñ"
        if sequence.prefix == "Ñ":
            prefix = "O"
        if sequence.prefix == "O":
            prefix = "P"
        if sequence.prefix == "P":
            prefix = "Q"
        if sequence.prefix == "Q":
            prefix = "R"
        if sequence.prefix == "R":
            prefix = "S"
        if sequence.prefix == "S":
            prefix = "T"
        if sequence.prefix == "T":
            prefix = "U"
        if sequence.prefix == "U":
            prefix = "V"
        if sequence.prefix == "V":
            prefix = "W"
        if sequence.prefix == "W":
            prefix = "X"
        if sequence.prefix == "X":
            prefix = "Y"
        if sequence.prefix == "Y":
            prefix = "Z"
        if prefix:
            sequence.sudo().write(
                {"prefix": prefix, "number_next": 0, "number_next_actual": 1}
            )
        else:
            sequence.sudo().write({"implementation": "standard"})
