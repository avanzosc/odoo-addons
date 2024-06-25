# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import pytz

from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    move_type_id = fields.Many2one(
        string="Move Type",
        comodel_name="move.type",
        related="product_id.categ_id.move_type_id",
        store=True,
    )
    days = fields.Integer(string="Days", compute="_compute_days", store=True)
    amount_days = fields.Float(
        string="Amount Days", compute="_compute_amount_days", store=True
    )
    average_weight = fields.Float(
        string="Average Weight",
        compute="_compute_average_weight",
        store=True,
        digits="Feep Decimal Precision",
    )
    farm_area = fields.Float(
        string="Farm Area", related="warehouse_id.farm_area", store=True
    )
    weight_area = fields.Float(
        string="Kgs./M2", compute="_compute_weight_area", store=True
    )
    type_category_id = fields.Many2one(
        string="Type Catergory",
        comodel_name="stock.picking.type.category",
        compute="_compute_type_category_id",
        store=True,
    )
    mother_id = fields.Many2one(compute="_compute_mother_id", store=True)
    cleaned_date = fields.Date(
        string="Cleaned Date", compute="_compute_mother_id", store=True
    )

    @api.depends(
        "picking_id",
        "picking_id.batch_id",
        "move_id",
        "move_id.inventory_id",
        "move_id.inventory_id.batch_id",
    )
    def _compute_mother_id(self):
        for line in self:
            mother = False
            if line.picking_id and line.picking_id.batch_id:
                mother = line.picking_id.batch_id
            elif (
                line.move_id
                and line.move_id.inventory_id
                and line.move_id.inventory_id.batch_id
            ):
                mother = line.move_id.inventory_id.batch_id
            line.mother_id = mother.id if mother else False
            line.cleaned_date = mother.cleaned_date if mother else False

    @api.depends(
        "picking_type_id",
        "picking_type_id.category_id",
        "production_id",
        "production_id.picking_type_id",
        "production_id.picking_type_id.category_id",
        "move_id",
        "move_id.raw_material_production_id",
        "move_id.raw_material_production_id.picking_type_id",
        "move_id.raw_material_production_id.picking_type_id.category_id",
    )
    def _compute_type_category_id(self):
        for line in self:
            categ = False
            if line.picking_id:
                categ = line.picking_type_id.category_id.id
            elif line.production_id:
                categ = line.production_id.picking_type_id.category_id.id
            elif line.move_id and line.move_id.production_id:
                categ = line.move_id.production_id.picking_type_id.category_id.id
            elif line.move_id and line.move_id.raw_material_production_id:
                categ = (
                    line.move_id.raw_material_production_id.picking_type_id.category_id.id
                )
            else:
                regularization = self.env.ref(
                    "stock_picking_batch_liquidation.picking_type_categ_regu"
                )
                if regularization:
                    categ = regularization.id
            line.type_category_id = categ

    @api.depends(
        "average_weight",
        "weight_area",
        "date",
        "mother_id",
        "mother_id.chick_units",
        "mother_id.move_line_ids",
        "mother_id.move_line_ids.state",
        "mother_id.move_line_ids.move_type_id",
        "mother_id.move_line_ids.download_unit",
        "mother_id.move_line_ids.date",
    )
    def _compute_weight_area(self):
        for line in self:
            weight_area = 0
            move_type3 = self.env.ref("stock_picking_batch_liquidation.move_type3")
            if line.move_type_id == move_type3:
                before_lines = line.mother_id.move_line_ids.filtered(
                    lambda c: c.state == "done"
                    and c.move_type_id == (move_type3)
                    and c.date < line.date
                )
                units = line.mother_id.chick_units
                if before_lines:
                    units = units - sum(before_lines.mapped("download_unit"))
                if line.farm_area != 0:
                    weight_area = units * line.average_weight / line.farm_area
            line.weight_area = weight_area

    @api.depends("download_unit", "qty_done")
    def _compute_average_weight(self):
        for line in self:
            average_weight = 0
            unit = self.env.ref("uom.product_uom_unit")
            if line.download_unit != 0 and line.product_uom_id != unit:
                average_weight = line.qty_done / line.download_unit
            line.average_weight = average_weight

    @api.depends("days", "download_unit")
    def _compute_amount_days(self):
        for line in self:
            line.amount_days = line.days * line.download_unit

    @api.depends("date", "mother_id", "mother_id.entry_date")
    def _compute_days(self):
        for line in self:
            days = 0
            if (
                line.mother_id
                and line.mother_id.entry_date
                and (line.date)
                and (line.mother_id.batch_type == "breeding")
            ):
                timezone = pytz.timezone(self._context.get("tz") or "UTC")
                line_date = line.date
                line_date = line_date.replace(tzinfo=pytz.timezone("UTC")).astimezone(
                    timezone
                )
                dif = line_date.date() - line.mother_id.entry_date
                days = dif.days - 1
            line.days = days

    @api.onchange("product_id", "product_uom_id", "lot_id")
    def _onchange_product_id(self):
        res = super()._onchange_product_id()
        if self.move_id.inventory_id and self.lot_id.average_price:
            self.standard_price = self.lot_id.average_price
        return res
