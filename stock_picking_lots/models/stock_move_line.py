# Copyright 2019 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    imei = fields.Char(string="imei")

    def _action_done(self):
        res = super()._action_done()
        for line in self:
            if line.imei and line.lot_id:
                line.lot_id.imei = line.imei
        return res
