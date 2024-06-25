# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    saca_id = fields.Many2one(
        string="Saca", comodel_name="saca", related="saca_line_id.saca_id", store="True"
    )
    saca_line_id = fields.Many2one(string="Saca Line", comodel_name="saca.line")
    paasa = fields.Boolean(string="PAASA", related="company_id.paasa", store=True)
    farm_id = fields.Many2one(
        string="Farm",
        comodel_name="res.partner",
        related="saca_line_id.farm_id",
        store=True,
    )
    breeding_id = fields.Many2one(
        string="Breeding",
        comodel_name="stock.picking.batch",
        related="saca_line_id.breeding_id",
        store=True,
    )
