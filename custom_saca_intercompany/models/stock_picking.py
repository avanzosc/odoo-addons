# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    saca_line_id = fields.Many2one(
        string="Saca Line",
        comodel_name="saca.line",
        compute="_compute_saca_line_id",
        store=True)
    saca_id = fields.Many2one(
        string="Saca",
        comodel_name="saca",
        related="saca_line_id.saca_id")
    tolvasa = fields.Boolean(
        string="Tolvasa",
        related="company_id.tolvasa",
        store=True)

    @api.depends("sale_id", "sale_id.saca_line_id", "purchase_id",
                 "purchase_id.saca_line_id")
    def _compute_saca_line_id(self):
        for line in self:
            line.saca_line_id = False
            if line.sale_id and line.sale_id.saca_line_id:
                line.saca_line_id = line.sale_id.saca_line_id.id
            elif line.purchase_id and line.purchase_id.saca_line_id:
                line.saca_line_id = line.purchase_id.saca_line_id.id
