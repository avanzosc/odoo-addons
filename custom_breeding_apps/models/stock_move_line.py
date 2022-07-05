# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from datetime import datetime
from dateutil import rrule
from odoo.exceptions import ValidationError


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    batch_id = fields.Many2one(
        string="Batch",
        comodel_name="stock.picking.batch",
        domain=lambda self: [
            ("batch_type", "=", "mother"),
            ("stage_id", "=",
             (self.env.ref("stock_picking_batch_mother.batch_stage8").id))])
    mother_id = fields.Many2one(
        string="Mother",
        comodel_name="stock.picking.batch",
        related="picking_id.batch_id",
        store=True)
    broken = fields.Integer(string="Broken")
    waste = fields.Integer(string="Waste")
    date_week = fields.Integer(
        string="Date Weeks",
        compute="_compute_date_week",
        store=True)
    laying_week = fields.Integer(
        string="Laying Weeks",
        compute="_compute_laying_week",
        store=True)
    stock = fields.Float(
        string="Stock",
        compute="_compute_stock")
    real_percentage = fields.Float(
        string="Real %",
        compute="_compute_real_percentage",
        store=True)
    estimate_laying = fields.Float(
        string="Laying estimate %",
        compute="_compute_estimate_laying")
    forecast = fields.Float(
        string="Forecast",
        compute="_compute_estimate_laying")
    difference = fields.Float(
        string="Difference",
        compute="_compute_difference")
    estimate_birth = fields.Float(
        string="Birth estimate %")
    birth_estimate_qty = fields.Float(
        string="Birth Estimate Quantity",
        compute="compute_birth_estimate_qty",
        store=True)
    standard_price = fields.Float(digits="Standard Cost Decimal Precision")
    rest = fields.Float(
        string="Rest",
        compute="_compute_rest",
        store=True)
    is_incubator = fields.Boolean(
        string="Incubator",
        related="picking_id.is_incubator", store=True)
    is_integration = fields.Boolean(
        string="Integration",
        related="picking_id.is_integration", store=True)
    is_reproductor = fields.Boolean(
        string="Reproductor",
        related="picking_id.is_reproductor", store=True)
    is_feed_flour = fields.Boolean(
        string="Feed/Flour",
        related="picking_id.is_feed_flour", store=True)
    is_medicine = fields.Boolean(
        string="Medicine",
        related="picking_id.is_medicine", store=True)
    warehouse_id = fields.Many2one(
        string="Origin Warehouse",
        comodel_name="stock.warehouse",
        related="location_id.warehouse_id",
        store=True)

    @api.depends("estimate_birth", "qty_done")
    def compute_birth_estimate_qty(self):
        for line in self:
            line.birth_estimate_qty = 0
            if line.estimate_birth and line.qty_done:
                line.birth_estimate_qty = (
                    line.estimate_birth * line.qty_done / 100)

    @api.depends("date")
    def _compute_date_week(self):
        for line in self:
            line.date_week = 0
            if line.date:
                start_date = datetime(
                    line.date.year, 1, 1, 0, 0).date()
                end_date = line.date.date()
                line.date_week = (
                    line.weeks_between(start_date, end_date))

    def _compute_stock(self):
        for line in self:
            line.stock = 0
            product = self.env["product.product"].search(
                [("is_hen", "=", True)], limit=1)
            if product:
                stock = line.batch_id.location_id.quant_ids.filtered(
                    lambda x: x.product_id == product)
                stock = sum(stock.mapped("available_quantity"))
                if stock:
                    line.stock = stock

    @api.depends("product_id", "location_id", "location_id.quant_ids",
                 "lot_id")
    def _compute_rest(self):
        for line in self:
            line.rest = 0
            if line.product_id and line.location_id and line.lot_id:
                origin = sum(self.env["stock.move.line"].search(
                    [("location_dest_id", "=", line.location_id.id),
                     ("product_id", "=", line.product_id.id),
                     ("lot_id", "=", line.lot_id.id)]).mapped("qty_done"))
                dest = sum(self.env["stock.move.line"].search(
                    [("location_id", "=", line.location_id.id),
                     ("product_id", "=", line.product_id.id),
                     ("lot_id", "=", line.lot_id.id)]).mapped("qty_done"))
                line.rest = origin - dest

    @api.depends("batch_id", "batch_id.start_laying_date", "date")
    def _compute_laying_week(self):
        for line in self:
            line.laying_week = 0
            if line.batch_id.start_laying_date:
                start_date = line.batch_id.start_laying_date
                end_date = line.date.date()
                line.laying_week = (
                    line.weeks_between(start_date, end_date))

    @api.depends("stock", "qty_done")
    def _compute_real_percentage(self):
        for line in self:
            if line.stock != 0:
                line.real_percentage = line.qty_done * 100 / line.stock

    @api.depends("batch_id", "batch_id.laying_rate_ids",
                 "batch_id.laying_rate_ids.week", "laying_week")
    def _compute_estimate_laying(self):
        for line in self:
            line.estimate_laying = 0
            line.forecast = 0
            if line.laying_week and line.batch_id.laying_rate_ids:
                rate = line.batch_id.laying_rate_ids.filtered(
                    lambda x: x.week == line.laying_week)
                if rate and rate.percentage_laying and rate.estimate_laying:
                    line.estimate_laying = rate.percentage_laying
                    line.forecast = rate.estimate_laying / 7

    def _compute_difference(self):
        for line in self:
            line.difference = 0
            if line.forecast and line.qty_done:
                line.difference = line.forecast - line.qty_done

    @api.onchange("batch_id", "location_id", "product_id")
    def onchange_lot_domain(self):
        domain = {}
        self.ensure_one()
        if self.batch_id and self.location_id and self.product_id:
            origin_lines = self.env["stock.move.line"].search(
                [("location_dest_id", "=", self.location_id.id),
                 ("product_id", "=", self.product_id.id),
                 ("batch_id", "=", self.batch_id.id)])
            dest_lines = self.env["stock.move.line"].search(
                [("location_id", "=", self.location_id.id),
                 ("product_id", "=", self.product_id.id),
                 ("batch_id", "=", self.batch_id.id)])
            lot = []
            for line in origin_lines:
                if line.lot_id.id not in lot:
                    origin = sum(origin_lines.filtered(
                        lambda x: x.lot_id == line.lot_id).mapped("qty_done"))
                    dest = sum(dest_lines.filtered(
                        lambda x: x.lot_id == line.lot_id).mapped("qty_done"))
                    dif = origin - dest
                    if dif > 0 and line.lot_id.product_qty > 0:
                        lot.append(line.lot_id.id)
            domain = {"domain": {"lot_id": [("id", "in", lot)]}}
        return domain

    @api.onchange("batch_id")
    def onchange_batch_id(self):
        if self.product_id and (
            self.batch_id) and (
                self.picking_id.egg_production is True):
            date_done = self.picking_id.custom_date_done
            if not date_done:
                raise ValidationError(
                    _("You must introduce the done date.")
                    )
            start_date = datetime(date_done.year, 1, 1, 0, 0).date()
            weeks = self.weeks_between(start_date, date_done)
            lot_name = u'{}{}{}'.format(
                self.batch_id.name, weeks, u'{}'.format(date_done.year)[2:])
            exists = self.env["stock.production.lot"].search(
                [("name", "=", lot_name),
                 ("product_id", "=", self.product_id.id)], limit=1)
            if exists:
                lot = exists
            else:
                lot = self.env["stock.production.lot"].create({
                    "name": lot_name,
                    "product_id": self.product_id.id,
                    "company_id": self.company_id.id,
                    "batch_id": self.batch_id.id})
            self.lot_id = lot.id

    @api.onchange("product_id")
    def onchange_product_id(self):
        if self.product_id:
            self.standard_price = self.product_id.standard_price

    def weeks_between(self, start_date, end_date):
        weeks = rrule.rrule(rrule.WEEKLY, dtstart=start_date, until=end_date)
        return weeks.count()
