# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockLot(models.Model):
    _inherit = "stock.lot"

    product_class_id = fields.Many2one(
        string="Pump type",
        comodel_name="product.class",
        related="product_id.product_class_id",
        store=True,
        copy=False,
    )
    application_type_id = fields.Many2one(
        string="Type of application",
        copy=False,
        comodel_name="stock.lot.type.application",
    )
