# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
import pytz


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    expiration_date = fields.Datetime(
        string="Warranty date")
    expiration_date_without_hour = fields.Date(
        string="Warranty date without_hour", copy=False, store=True,
        compute="_compute_expiration_date_without_hour")

    @api.depends("expiration_date")
    def _compute_expiration_date_without_hour(self):
        local_tz = pytz.timezone(self.env.user.tz or 'UTC')
        for lot in self:
            if lot.expiration_date:
                local_dt = lot.expiration_date.replace(
                    tzinfo=pytz.utc).astimezone(local_tz)
                lot.expiration_date_without_hour = local_dt.date()
