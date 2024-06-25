# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import pytz

from odoo import api, fields, models


class StockValuationLayer(models.Model):
    _inherit = "stock.valuation.layer"

    categ_id = fields.Many2one(store=True, copy=False)
    lineal_id = fields.Many2one(
        string="Lineal",
        comodel_name="product.lineal",
        related="product_id.lineal_id",
        store=True,
        copy=False,
    )
    create_date_without_hour = fields.Date(
        string="Create date",
        copy=False,
        store=True,
        compute="_compute_create_date_without_hour",
    )

    @api.depends("create_date")
    def _compute_create_date_without_hour(self):
        local_tz = pytz.timezone(self.env.user.tz or "UTC")
        for layer in self:
            if layer.create_date:
                local_dt = layer.create_date.replace(tzinfo=pytz.utc).astimezone(
                    local_tz
                )
                layer.create_date_without_hour = local_dt.date()
