# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    saca_id = fields.Many2one(
        string="Saca",
        comodel_name="saca",
        related="saca_line_id.saca_id",
        store="True")
    saca_line_id = fields.Many2one(
        string="Saca Line",
        comodel_name="saca.line")
