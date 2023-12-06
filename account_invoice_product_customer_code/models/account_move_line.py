# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _compute_customer_product_code(self):
        for line in self:
            product_code = ""
            if (
                line.product_id
                and line.product_id.customer_code_ids
                and line.move_id.partner_id
            ):
                partner = (
                    line.move_id.partner_id
                    if not line.move_id.partner_id.parent_id
                    else line.move_id.partner_id.parent_id
                )
                codes = line.product_id.customer_code_ids.filtered(
                    lambda x: x.partner_id == partner
                )
                if codes:
                    for code in codes:
                        product_code = code.customer_code
            line.customer_product_code = product_code

    def _compute_product_display_name(self):
        for line in self:
            product_display_name = line.product_id.display_name
            if (
                line.move_id.move_type == "out_invoice"
                and line.product_id.default_code
                and line.customer_product_code
                and line.product_id.default_code in product_display_name
            ):
                new_value = product_display_name.replace(
                    line.product_id.default_code, line.customer_product_code
                )
                product_display_name = new_value
            line.product_display_name = product_display_name

    customer_product_code = fields.Char(
        string="Customer product code", compute="_compute_customer_product_code"
    )
    product_display_name = fields.Char(
        string="Product display name", compute="_compute_product_display_name"
    )
