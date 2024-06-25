# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockReturnPicking(models.TransientModel):
    _inherit = "stock.return.picking"

    def _create_returns(self):
        new_picking_id, picking_type_id = super()._create_returns()
        new_picking = self.env["stock.picking"].browse(new_picking_id)
        if "active_id" in self.env.context:
            active = self.env["stock.picking"].browse(self.env.context["active_id"])
            if active and active.batch_id:
                new_picking.batch_id = active.batch_id.id
                new_picking.custom_date_done = fields.Datetime.now()
        for line in new_picking.move_line_ids_without_package:
            if line.move_id and line.move_id.standard_price:
                line.standard_price = line.move_id.standard_price
        return new_picking_id, picking_type_id
