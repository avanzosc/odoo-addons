# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    vat_price = fields.Float(
        string='VAT price', related='product_id.vat_price', store=True)
