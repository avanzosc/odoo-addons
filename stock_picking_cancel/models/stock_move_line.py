# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models
from odoo.exceptions import UserError


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _refresh_quants_by_picking_cancelation(self):
        quant_obj = self.env["stock.quant"]
        cond = self._quant_condition_for_picking_cancelation(self.location_dest_id)
        quant = quant_obj.search(cond)
        if len(quant) > 1:
            raise UserError(
                _(
                    "More than 1 quant found for move line with id: {}, and "
                    "condition: {}"
                ).format(self.id, cond)
            )
        if quant:
            quant.sudo().quantity = quant.quantity - self.qty_done
        cond = self._quant_condition_for_picking_cancelation(self.location_id)
        quant = quant_obj.search(cond)
        if len(quant) > 1:
            raise UserError(
                _(
                    "More than 1 quant found for move line with id: {}, and "
                    "condition: {}"
                ).format(self.id, cond)
            )
        if quant:
            quant.sudo().quantity = quant.quantity + self.qty_done

    def _quant_condition_for_picking_cancelation(self, location):
        cond = [
            ("product_id", "=", self.product_id.id),
            ("location_id", "=", location.id),
        ]
        if location.company_id:
            ("company_id", "=", location.company_id.id)
        if self.lot_id:
            cond.append(("lot_id", "=", self.lot_id.id))
        else:
            cond.append(("lot_id", "=", False))
        if self.package_id:
            cond.append(("package_id", "=", self.package_id.id))
        if self.result_package_id:
            cond.append(("package_id", "=", self.result_package_id.id))
        if not self.package_id and not self.result_package_id:
            cond.append(("package_id", "=", False))
        if self.owner_id:
            cond.append(("owner_id", "=", self.owner_id.id))
        else:
            cond.append(("owner_id", "=", False))
        return cond
