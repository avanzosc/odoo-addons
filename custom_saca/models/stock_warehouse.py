# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    main_scale = fields.Many2one(string="Scale", comodel_name="main.scale")
