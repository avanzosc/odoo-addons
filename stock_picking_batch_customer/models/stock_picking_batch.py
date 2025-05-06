# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    customer_id = fields.Many2one(string="Customer", comodel_name="res.partner")
