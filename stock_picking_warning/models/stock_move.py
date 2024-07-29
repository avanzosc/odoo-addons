# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.onchange("product_id", "picking_type_id")
    def _onchange_product_id(self):
        result = super()._onchange_product_id()
        prod = self.product_id.with_context(lang=self._get_lang())
        if prod:
            res = {}
            if (
                prod.out_picking_warn == "warning"
                and self.picking_type_id.code == "outgoing"
            ):
                warning = {
                    "title": _("Product out picking warning"),
                    "message": prod.out_picking_warn_msg,
                }
                res["warning"] = warning
            if (
                prod.in_picking_warn == "warning"
                and self.picking_type_id.code == "incoming"
            ):
                warning = {
                    "title": _("Product in picking warning"),
                    "message": prod.in_picking_warn_msg,
                }
                res["warning"] = warning
            if res:
                return res
        return result
