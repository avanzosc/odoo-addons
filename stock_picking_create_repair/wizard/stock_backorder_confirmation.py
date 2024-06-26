# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models
from odoo.exceptions import ValidationError


class StockBackorderConfirmation(models.TransientModel):
    _inherit = "stock.backorder.confirmation"

    def process(self):
        result = super().process()
        pickings = self.pick_ids.filtered(
            lambda x: x.picking_type_id.code == "outgoing"
            and x.is_repair
            and x.sale_order_id
        )
        if pickings:
            pickings.with_context(
                created_new_picking=True
            )._put_realized_moves_in_repairs()
        return result

    def process_cancel_backorder(self):
        result = super().process_cancel_backorder()
        pickings = self.pick_ids.filtered(
            lambda x: x.picking_type_id.code == "outgoing"
            and x.is_repair
            and x.sale_order_id
        )
        if pickings:
            for picking in pickings:
                raise ValidationError(
                    _(
                        "The out picking {} is for repairs, you must create a "
                        "partial order delivery"
                    ).format(picking.name)
                )
            pickings._put_realized_moves_in_repairs()
        return result
