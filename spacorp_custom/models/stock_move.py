# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    market_id = fields.Many2one(
        string="Market",
        comodel_name="res.partner.market",
        related="picking_id.market_id",
        store=True,
    )
    market_sector_id = fields.Many2one(
        string="Market sector",
        comodel_name="res.partner.market.sector",
        related="picking_id.market_sector_id",
        store=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        moves = super().create(vals_list)
        for move in moves:
            move.picking_id.update_division_in_pickings()
        return moves

    def _get_new_picking_values(self):
        result = super()._get_new_picking_values()
        if "origin" in result and result.get("origin", False):
            cond = [("name", "=", result.get("origin"))]
            sale = self.env["sale.order"].search(cond, limit=1)
            if sale and sale.team_id:
                result["team_id"] = sale.team_id.id
            if sale and sale.contact_email_person_id:
                result["contact_email_person_id"] = sale.contact_email_person_id.id
        return result
