# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    saca_id = fields.Many2one(
        string="Saca",
        comodel_name="saca",
        related="auto_purchase_line_id.saca_id",
        store=True)
    saca_line_id = fields.Many2one(
        string="Saca Line",
        comodel_name="saca.line",
        related="auto_purchase_line_id.saca_line_id",
        store=True)
    farm_id = fields.Many2one(
        string="Farm",
        comodel_name="res.partner",
        related="auto_purchase_line_id.farm_id",
        store=True)
    farmer_id = fields.Many2one(
        string="Farmer",
        comodel_name="res.partner",
        related="auto_purchase_line_id.farmer_id",
        store=True)
