# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        result = super(StockPicking, self).button_validate()
        for picking in self.filtered(
                lambda x: x.picking_type_id.code == "incoming"):
            for picking in self:
                lines = picking.move_line_ids.filtered(
                    lambda z: z.lot_id and z.state == "done")
                for line in lines:
                    if line.move_id.purchase_line_id:
                        purchase_line = line.move_id.purchase_line_id
                        line.lot_id.write(
                            {"purchase_price": purchase_line.price_unit,
                             "supplier_id":
                             purchase_line.order_id.partner_id.id})
        return result
