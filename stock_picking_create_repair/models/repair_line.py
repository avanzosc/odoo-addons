# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class RepairLine(models.Model):
    _inherit = "repair.line"

    @api.model
    def create(self, vals):
        repair_lines = super().create(vals)
        repair_lines._put_amount_untaxed_in_price_in_sale_budget()
        return repair_lines

    def write(self, vals):
        res = super().write(vals)
        if "product_uom_qty" in vals or "price_unit" in vals:
            self._put_amount_untaxed_in_price_in_sale_budget()
        return res

    def _put_amount_untaxed_in_price_in_sale_budget(self):
        for line in self.filtered(
            lambda x: x.repair_id.state == "draft"
            and x.type == "add"
            and x.repair_id.sale_order_id
            and x.repair_id.sale_order_id.is_repair
        ):
            line.repair_id.price_in_sale_budget = (
                0
                if not line.repair_id.product_qty
                else line.repair_id.amount_untaxed / line.repair_id.product_qty
            )
