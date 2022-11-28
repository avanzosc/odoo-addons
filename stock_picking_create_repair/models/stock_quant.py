# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    def _gather(self, product_id, location_id, lot_id=None, package_id=None,
                owner_id=None, strict=False):
        quants = super(StockQuant, self)._gather(
            product_id, location_id, lot_id=lot_id, package_id=package_id,
            owner_id=owner_id, strict=strict)
        if "default_quants" not in self.env.context:
            return quants
        my_quants = self.env['stock.quant']
        default_quants = self.env.context.get("default_quants")
        for quant in quants:
            if quant in default_quants:
                my_quants += quant
        return my_quants
