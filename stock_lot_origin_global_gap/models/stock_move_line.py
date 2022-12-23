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
