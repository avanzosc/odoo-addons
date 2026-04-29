from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _action_done(self):
        pending = [
            (ml.package_id, ml.move_id.picking_id.partner_id)
            for ml in self
            if ml.package_id and ml.move_id.picking_id and not ml.package_id.partner_id
        ]
        res = super()._action_done()
        for package, partner in pending:
            if not package.partner_id:
                package.partner_id = partner
        return res
