# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def name_get(self):
        res = []
        for move in self:
            res.append(
                (move.id, "[{}] {}".format(move.product_id.code, move.product_id.name))
            )
        return res
