# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    country_id = fields.Many2one(
        string="Origin", comodel_name="res.country")
    global_gap = fields.Char(
        string="Global Gap")
    lot_country_id = fields.Many2one(
        string="Lot Origin", comodel_name="res.country", copy=False,
        store=True, related="lot_id.country_id")
    lot_global_gap = fields.Char(
        string="Lot Global Gap", related="lot_id.ref", copy=False,
        store=True)
    lot_country_to_print = fields.Char(
        string="Lot Origin to print",
        compute="_compute_country_global_gap_to_print")
    lot_global_gap_to_print = fields.Char(
        string="Lot Global Gap to print",
        compute="_compute_country_global_gap_to_print")

    def _compute_country_global_gap_to_print(self):
        for line in self:
            lot_country_to_print = ""
            lot_global_gap_to_print = ""
            if not line.move_id.created_production_id:
                if line.lot_country_id:
                    lot_country_to_print = line.lot_country_id.name
                if line.lot_global_gap:
                    lot_global_gap_to_print = line.lot_global_gap
            else:
                move_lines = line.move_id.created_production_id.move_raw_ids
                move_lines = move_lines.filtered(
                    lambda x: x.state != "cancel" and
                    x.product_id.show_origin_global_gap_in_documents)
                for ml in move_lines:
                    for move_line in ml.move_line_ids.filtered(
                            lambda z: z.lot_id):
                        if move_line.lot_id.country_id:
                            if not lot_country_to_print:
                                lot_country_to_print = (
                                    move_line.lot_id.country_id.name)
                            else:
                                lot_country_to_print = u"{}, {}".format(
                                    lot_country_to_print,
                                    move_line.lot_id.country_id.name)
                        if move_line.lot_id.ref:
                            if not lot_global_gap_to_print:
                                lot_global_gap_to_print = move_line.lot_id.ref
                            else:
                                lot_global_gap_to_print = u"{}, {}".format(
                                    lot_global_gap_to_print,
                                    move_line.lot_id.ref)
            line.lot_country_to_print = lot_country_to_print
            line.lot_global_gap_to_print = lot_global_gap_to_print

    def _create_and_assign_production_lot(self):
        result = super(StockMoveLine, self)._create_and_assign_production_lot()
        for line in self.filtered(
            lambda x: x.lot_id and x.lot_name and x.picking_id and
                x.picking_id.picking_type_id.code == "incoming"):
            vals = {}
            if line.country_id:
                vals["country_id"] = line.country_id.id
            if line.global_gap:
                vals["ref"] = line.global_gap
            if vals:
                line.lot_id.write(vals)
        return result
