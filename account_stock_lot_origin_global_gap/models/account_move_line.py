# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    lot_id = fields.Many2one(
        string="Lot", comodel_name="stock.lot", compute="_compute_country_global_gap"
    )
    lot_country_id = fields.Many2one(
        string="Lot Origin",
        comodel_name="res.country",
        compute="_compute_country_global_gap",
    )
    lot_global_gap = fields.Char(
        string="Lot Global Gap", compute="_compute_country_global_gap"
    )
    lot_country_to_print = fields.Text(
        string="Lot Origin OF", compute="_compute_country_global_gap"
    )
    lot_global_gap_to_print = fields.Text(
        string="Lot Global Gap OF", compute="_compute_country_global_gap"
    )
    lot_country_gloval_gap_of = fields.Text(
        string="Lot Origin/Global Gap OF", compute="_compute_country_global_gap"
    )

    def _compute_country_global_gap(self):
        for line in self:
            lot = self.env["stock.lot"]
            lot_country = self.env["res.country"]
            stock_moves = self.env["stock.move.line"]

            lot_global_gap = ""
            lot_country_to_print = ""
            lot_global_gap_to_print = ""
            lot_country_gloval_gap_of = ""
            if line.move_line_ids:
                stock_moves = line.move_line_ids
            if (
                not line.move_line_ids
                and line.purchase_line_id
                and line.purchase_line_id.move_ids
            ):
                stock_moves = line.purchase_line_id.move_ids
            for stock_move in stock_moves:
                for move_line in stock_move.move_line_ids.filtered(lambda x: x.lot_id):
                    if move_line.lot_country_gloval_gap_of:
                        lot = move_line.lot_id
                        lot_country_to_print = move_line.lot_country_to_print
                        lot_global_gap_to_print = move_line.lot_global_gap_to_print
                        lot_country_gloval_gap_of = move_line.lot_country_gloval_gap_of
                    else:
                        if move_line.lot_id.country_id or move_line.lot_id.ref:
                            lot = move_line.lot_id
                            lot_country = move_line.lot_id.country_id
                            lot_global_gap = move_line.lot_id.ref
                            lot_global_gap_to_print = move_line.lot_id.ref
                            if move_line.lot_id.country_id:
                                lot_country_to_print = move_line.lot_id.country_id.name
            line.lot_id = lot.id if lot else lot
            line.lot_country_id = lot_country.id if lot_country else lot_country
            line.lot_global_gap = lot_global_gap
            line.lot_country_to_print = lot_country_to_print
            line.lot_global_gap_to_print = lot_global_gap_to_print
            line.lot_country_gloval_gap_of = lot_country_gloval_gap_of
