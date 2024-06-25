# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockProductionLotTypeApplication(models.Model):
    _name = "stock.production.lot.type.application"
    _description = "Type of application"

    name = fields.Char(string="Description", copy=False)
