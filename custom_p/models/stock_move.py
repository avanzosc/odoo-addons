from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _assign_picking_post_process(self, new=False):
        result = super()._assign_picking_post_process(new=new)
        if new:
            pickings = self.mapped("picking_id")
            for picking in pickings:
                if (
                    picking.group_id
                    and picking.group_id.sale_id
                    and not picking.sale_id
                ):
                    picking._compute_field_value(picking._fields["sale_id"])
        return result
