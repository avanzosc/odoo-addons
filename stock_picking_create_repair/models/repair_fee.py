# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class RepairFee(models.Model):
    _inherit = "repair.fee"

    @api.model
    def _get_default_product_id(self):
        cond = [("default_product_manufacturing_operations", '=', True)]
        product = self.env["product.product"].search(cond, limit=1)
        if product:
            return product

    product_id = fields.Many2one(
        default=_get_default_product_id)

    @api.model
    def create(self, vals):
        repair_fees = super(RepairFee, self).create(vals)
        repair_fees._put_amount_untaxed_in_price_in_sale_budget()
        return repair_fees

    def write(self, vals):
        res = super(RepairFee, self).write(vals)
        if "product_uom_qty" in vals or "price_unit" in vals:
            self._put_amount_untaxed_in_price_in_sale_budget()
        return res

    def _put_amount_untaxed_in_price_in_sale_budget(self):
        for fee in self.filtered(lambda x: x.repair_id.state == "draft" and
                                 x.repair_id.sale_order_id and
                                 x.repair_id.sale_order_id.is_repair):
            fee.repair_id.price_in_sale_budget = fee.repair_id.amount_untaxed
