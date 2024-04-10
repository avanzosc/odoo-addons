# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    country_id = fields.Many2one(string="Origin", comodel_name="res.country")
    global_gap = fields.Char(string="Global Gap")
    lot_country_id = fields.Many2one(
        string="Lot Origin",
        comodel_name="res.country",
        copy=False,
        store=True,
        related="lot_id.country_id",
    )
    lot_global_gap = fields.Char(
        string="Lot Global Gap", related="lot_id.ref", copy=False, store=True
    )
    lot_country_to_print = fields.Text(
        string="Lot Origin OF", compute="_compute_country_global_gap_to_print"
    )
    lot_global_gap_to_print = fields.Text(
        string="Lot Global Gap OF", compute="_compute_country_global_gap_to_print"
    )
    lot_country_gloval_gap_of = fields.Text(
        string="Lot Origin/Global Gap OF",
        compute="_compute_country_global_gap_to_print",
    )

    def _compute_country_global_gap_to_print(self):
        for line in self:
            lot_country_to_print = ""
            lot_global_gap_to_print = ""
            lot_country_gloval_gap_of = ""
            if line.lot_id and (
                line.lot_id.lot_country_of or line.lot_id.lot_global_gap_of
            ):
                lot_country_to_print = line.lot_id.lot_country_of
                lot_global_gap_to_print = line.lot_id.lot_global_gap_of
                lot_country_gloval_gap_of = line.lot_id.lot_country_gloval_gap_of
            else:
                if line.lot_country_id:
                    lot_country_to_print = line.lot_country_id.name
                if line.lot_global_gap:
                    lot_global_gap_to_print = line.lot_global_gap
            line.lot_country_to_print = lot_country_to_print
            line.lot_global_gap_to_print = lot_global_gap_to_print
            line.lot_country_gloval_gap_of = lot_country_gloval_gap_of

    def _get_name_country_global_gap_of(
        self, country_of, global_gap_of, country_gloval_gap_of
    ):
        if not self.lot_id.country_id:
            country_of = ",\n" if not country_of else "{},\n".format(country_of)
        else:
            country_of = (
                "{},\n".format(self.lot_id.country_id.name)
                if not country_of
                else "{}{},\n".format(country_of, self.lot_id.country_id.name)
            )
        if not self.lot_id.ref:
            global_gap_of = (
                ",\n" if not global_gap_of else "{},\n".format(global_gap_of)
            )
        else:
            global_gap_of = (
                "{},\n".format(self.lot_id.ref)
                if not global_gap_of
                else "{}{},\n".format(global_gap_of, self.lot_id.ref)
            )
        if not country_gloval_gap_of:
            country_gloval_gap_of = "{} / {}".format(
                "" if not self.lot_id.country_id else self.lot_id.country_id.name,
                self.lot_id.ref,
            )
        else:
            country_gloval_gap_of = "{}\n{} / {}".format(
                country_gloval_gap_of,
                "" if not self.lot_id.country_id else self.lot_id.country_id.name,
                self.lot_id.ref,
            )
        return country_of, global_gap_of, country_gloval_gap_of

    def _create_and_assign_production_lot(self):
        result = super()._create_and_assign_production_lot()
        for line in self.filtered(
            lambda x: x.lot_id
            and x.lot_name
            and x.picking_id
            and x.picking_id.picking_type_id.code == "incoming"
        ):
            vals = {}
            if line.country_id:
                vals["country_id"] = line.country_id.id
            if line.global_gap:
                vals["ref"] = line.global_gap
            if vals:
                line.lot_id.write(vals)
        return result
