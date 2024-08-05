# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        for picking in self:
            moves = False
            if picking.picking_type_id.code == "outgoing":
                moves = picking.mapped("move_ids").filtered(
                    lambda x: x.product_id and x.product_id.out_picking_warn == "block"
                )
            if picking.picking_type_id.code == "incoming":
                moves = picking.mapped("move_ids").filtered(
                    lambda z: z.product_id and z.product_id.in_picking_warn == "block"
                )
            if moves:
                err = ""
                for move in moves:
                    err += "{}{}{}: {}\n".format(
                        err,
                        _("Product "),
                        move.product_id.name,
                        (
                            move.product_id.out_picking_warn_msg
                            if picking.picking_type_id.code == "outgoing"
                            else move.product_id.in_picking_warn_msg
                        ),
                    )
                raise ValidationError(err)
        return super().button_validate()
