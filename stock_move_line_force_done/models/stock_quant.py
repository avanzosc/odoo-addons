# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api
from odoo.tools.float_utils import float_compare


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.model
    def _update_reserved_quantity(self, product_id, location_id, quantity,
                                  lot_id=None, package_id=None, owner_id=None,
                                  strict=False):
        self = self.sudo()
        rounding = product_id.uom_id.rounding
        quants = self._gather(
            product_id, location_id, lot_id=lot_id, package_id=package_id,
            owner_id=owner_id, strict=strict)
        if float_compare(quantity, 0, precision_rounding=rounding) < 0:
            available_quantity = sum(quants.mapped('reserved_quantity'))
            if float_compare(
                abs(quantity), available_quantity,
                    precision_rounding=rounding) > 0:
                if len(quants) == 1:
                    if quantity < 0:
                        quantity = quantity * -1
                    my_quantity = available_quantity + quantity
                    quants.write({'reserved_quantity': my_quantity})
        return super(StockQuant, self)._update_reserved_quantity(
            product_id, location_id, quantity, lot_id=lot_id,
            package_id=package_id, owner_id=owner_id, strict=strict)
