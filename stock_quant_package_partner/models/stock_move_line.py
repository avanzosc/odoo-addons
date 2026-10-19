from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _action_done(self):
        res = super()._action_done()
        for ml in self.exists():
            if ml.package_id and ml.move_id.picking_id and not ml.package_id.partner_id:
                ml.package_id.partner_id = ml.move_id.picking_id.partner_id

        return res
