# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductSupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    consumed_last_twelve_months = fields.Float(
        string="Consumed last twelve months",
        digits="Product Unit of Measure",
        compute="_compute_months_qtys_quantities",
    )
    months_with_stock = fields.Integer(
        string="Months with stock",
        compute="_compute_months_qtys_quantities",
    )

    def _compute_months_qtys_quantities(self):
        for supplierinfo in self:
            supplierinfo.consumed_last_twelve_months = (
                supplierinfo.product_id.consumed_last_twelve_months
                if supplierinfo.product_id
                else supplierinfo.product_tmpl_id.consumed_last_twelve_months
            )
            supplierinfo.months_with_stock = (
                supplierinfo.product_id.months_with_stock
                if supplierinfo.product_id
                else supplierinfo.product_tmpl_id.months_with_stock
            )
