# Copyright Bernabé Olavarrieta - Alquemy
# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"
    _order = "use_date ASC, expiration_date ASC, id ASC"

    expiration_date = fields.Datetime(
        string="Expiration Date",
        related="lot_id.expiration_date",
        store=True,
        readonly=True,
    )
    use_date = fields.Datetime(
        string="Best before Date", related="lot_id.use_date", store=True, readonly=True
    )
    removal_date = fields.Datetime(
        string="Removal Date", related="lot_id.removal_date", store=True, readonly=True
    )
    alert_date = fields.Datetime(
        string="Alert Date", related="lot_id.alert_date", store=True, readonly=True
    )
