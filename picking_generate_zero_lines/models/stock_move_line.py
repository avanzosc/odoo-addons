from odoo import _, models
from odoo.exceptions import UserError


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def action_done(self):
        for line in self:
            if line.product_id.tracking != "none" and (
                not line.lot_id or line.lot_name
            ):
                raise UserError(
                    _("You need to supply a Lot/Serial number for product %s")
                    % (line.product_id.display_name)
                )
        return super().action_done()
