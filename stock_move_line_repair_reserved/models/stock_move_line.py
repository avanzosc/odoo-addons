from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _action_done(self):
        res = super()._action_done()
        Quant = self.env["stock.quant"]

        for move_line in self:

            quants = Quant.browse()

            quants |= Quant._gather(
                move_line.product_id,
                move_line.location_id,
                lot_id=move_line.lot_id,
                package_id=move_line.package_id,
                owner_id=move_line.owner_id,
                strict=True,
            )

            quants |= Quant._gather(
                move_line.product_id,
                move_line.location_dest_id,
                lot_id=move_line.lot_id,
                package_id=move_line.result_package_id or move_line.package_id,
                owner_id=move_line.owner_id,
                strict=True,
            )

            if quants:
                quants.action_repair_reserved_quantity()

        return res
