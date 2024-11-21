# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def button_return_picking(self):
        for purchase in self:
            if (
                purchase.picking_ids
                and len(purchase.picking_ids) == 1
                and purchase.picking_ids[:1].state == "done"
            ):
                wiz_obj = self.env["stock.return.picking"]
                vals = {"picking_id": purchase.picking_ids[:1].id}
                wiz = wiz_obj.create(vals)
                wiz._onchange_picking_id()
                result = wiz.sudo().create_returns()
                return result
            else:
                raise UserError(_("You can only return one done picking."))
