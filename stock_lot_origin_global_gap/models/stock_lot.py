# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockLot(models.Model):
    _inherit = "stock.lot"

    country_id = fields.Many2one(string="Origin", comodel_name="res.country")
    ref = fields.Char(string="Global Gap")
    lot_country_of = fields.Text(
        string="Lot Origin OF", compute="_compute_country_global_gap_of"
    )
    lot_global_gap_of = fields.Text(
        string="Lot Global Gap OF", compute="_compute_country_global_gap_of"
    )
    lot_country_gloval_gap_of = fields.Text(
        string="Lot Origin/Global Gap OF", compute="_compute_country_global_gap_of"
    )

    def _compute_country_global_gap_of(self):
        for lot in self:
            country_of = ""
            global_gap_of = ""
            country_gloval_gap_of = ""
            cond = [("lot_producing_id", "=", lot.id)]
            production = self.env["mrp.production"].search(cond, limit=1)
            if production:
                move_lines = production.move_raw_ids
                move_lines = move_lines.filtered(
                    lambda x: x.state != "cancel"
                    and x.product_id.show_origin_global_gap_in_documents
                )
                for ml in move_lines:
                    for move_line in ml.move_line_ids.filtered(
                        lambda z: z.lot_id and (z.lot_id.country_id or z.lot_id.ref)
                    ):
                        (
                            country_of,
                            global_gap_of,
                            country_gloval_gap_of,
                        ) = move_line._get_name_country_global_gap_of(
                            country_of, global_gap_of, country_gloval_gap_of
                        )
            lot.lot_country_of = country_of
            lot.lot_global_gap_of = global_gap_of
            lot.lot_country_gloval_gap_of = country_gloval_gap_of
