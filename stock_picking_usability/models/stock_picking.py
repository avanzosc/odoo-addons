# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _action_generate_backorder_wizard(self, show_transfers=False):
        warning = ""
        if len(self) == 1:
            moves = self.move_ids_without_package.filtered(
                lambda x: x.quantity_done > 0 and x.quantity_done != x.product_uom_qty
            )
            if moves:
                for move in moves:
                    warning_text = _("Product: {}, quantity not send: {}").format(
                        move.product_id.name,
                        str(move.product_uom_qty - move.quantity_done),
                    )
                    warning = (
                        warning_text
                        if not warning
                        else "{} \n{}".format(warning, warning_text)
                    )
        if not warning:
            return super()._action_generate_backorder_wizard(
                show_transfers=show_transfers
            )
        return super(
            StockPicking, self.with_context(warning_not_all_send=warning)
        )._action_generate_backorder_wizard(show_transfers=show_transfers)
