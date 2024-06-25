# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

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
        comodel_name="stock.production.lot.type.application",
    )
