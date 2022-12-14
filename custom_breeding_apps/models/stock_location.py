# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    is_incubator = fields.Boolean(
        string="Incubator",
        related="warehouse_id.is_incubator", store=True)
    is_integration = fields.Boolean(
        string="Integration",
        related="warehouse_id.is_integration", store=True)
    is_reproductor = fields.Boolean(
        string="Reproductor",
        related="warehouse_id.is_reproductor", store=True)
    is_feed_flour = fields.Boolean(
        string="Feed/Flour",
        related="warehouse_id.is_feed_flour", store=True)
    is_medicine = fields.Boolean(
        string="Medicine",
        related="warehouse_id.is_medicine", store=True)
