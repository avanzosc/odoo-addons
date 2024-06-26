# Copyright 2020 Alfredo de la Fuente - Avanzosc S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.onchange("product_id")
    def onchange_product_id(self):
        result = super().onchange_product_id()
        if not self.product_id or not self.order_id.partner_id:
            return result
        if not result:
            result = {}
        result = self._round_line_qty(result)
        return result

    @api.onchange("product_qty")
    def onchange_product_qty_for_round(self):
        if not self.product_id or not self.order_id.partner_id:
            return
        result = self._round_line_qty({})
        return result

    def _round_line_qty(self, result):
        line = self.with_company(self.company_id)
        params = {"order_id": line.order_id}
        seller = line.product_id._select_seller(
            partner_id=self.order_id.partner_id,
            quantity=line.product_qty,
            date=(
                (line.order_id.date_order and line.order_id.date_order.date())
                or (fields.Date.context_today(line))
            ),
            uom_id=line.product_uom,
            params=params,
        )
        if seller and seller.round_quantity_purchase:
            round_qty = seller.round_quantity_purchase
            rounded = False
            if round_qty > 0:
                initial_qty = line.product_qty if line.product_qty else 1
                resto = initial_qty % round_qty
                while resto != 0:
                    rounded = True
                    initial_qty += 1
                    resto = initial_qty % round_qty
                self.product_qty = initial_qty
            if rounded:
                message = _(
                    "THE QUANTITY TO BUY has been rounded to a" " multiple of {}"
                ).format(round_qty)
                if (
                    "warning" in result
                    and result.get("warning", False)
                    and message not in result.get("warning").get("message")
                ):
                    w = result.get("warning")
                    m = w.get("message")
                    new_message = "{}\n{}".format(message, m)
                    result["warning"]["message"] = new_message
                else:
                    title = _("WARNING for {}").format(line.product_id.name)
                    result["warning"] = {"title": title, "message": message}
        return result
