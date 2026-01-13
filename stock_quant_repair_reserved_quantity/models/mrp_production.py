from odoo import models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def button_mark_done(self):
        res = super().button_mark_done()

        Quant = self.env["stock.quant"]

        for production in self:
            move_lines = production.move_raw_ids.mapped(
                "move_line_ids"
            ) | production.move_finished_ids.mapped("move_line_ids")

            quants = Quant.browse()

            for ml in move_lines:
                quants |= Quant._gather(
                    ml.product_id,
                    ml.location_id,
                    lot_id=ml.lot_id,
                    package_id=ml.package_id,
                    owner_id=ml.owner_id,
                    strict=True,
                )

                quants |= Quant._gather(
                    ml.product_id,
                    ml.location_dest_id,
                    lot_id=ml.lot_id,
                    package_id=ml.result_package_id or ml.package_id,
                    owner_id=ml.owner_id,
                    strict=True,
                )

            if quants:
                quants.action_repair_reserved_quantity()

        return res
