# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    not_update_price_from_order = fields.Boolean(
        string="Not Update Price From Order",
        related="name.not_update_price_from_order",
        readonly=False,
        store=True,
    )
    not_update_price_from_invoice = fields.Boolean(
        string="Not Update Price From Invoice",
        related="name.not_update_price_from_invoice",
        readonly=False,
        store=True,
    )
