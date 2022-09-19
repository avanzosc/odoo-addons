# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from datetime import datetime, timedelta
from dateutil import rrule
from odoo.exceptions import ValidationError


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _default_get_product_id(self):
        result = False
        product = self.env["product.product"].search(
            [("egg", "=", True)], limit=1)
        if product and "default_picking_id" in self.env.context and (
            self.env["stock.picking"].search(
                [("id", "=", self.env.context["default_picking_id"])],
                limit=1).burden_to_incubator):
            result = product.id
        return result

    source_document = fields.Char(string="Source Document")
    product_id = fields.Many2one(default=_default_get_product_id)
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
    birth_estimate_qty = fields.Integer(
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
    download_unit = fields.Integer(
        string="Units")
    lot_display_name = fields.Char(
        string="Lot/Serial Nº Name",
        related="lot_id.name",
        store=True)

    @api.depends("estimate_birth", "download_unit")
    def compute_birth_estimate_qty(self):
        for line in self:
            line.birth_estimate_qty = 0
            if line.estimate_birth and line.download_unit:
                line.birth_estimate_qty = (
                    line.estimate_birth * line.download_unit / 100)

    def calculate_weeks_start(self, start_date):
        self.ensure_one()
        weekday = start_date.weekday()
        if weekday <= 3:
            return start_date - timedelta(days=weekday)
        else:
            return start_date + timedelta(days=(7-weekday))

    @api.depends("date")
    def _compute_date_week(self):
        for line in self:
            line.date_week = 0
            if line.date:
                start_date = datetime(
                    line.date.year, 1, 1, 0, 0).date()
                start_date = line.calculate_weeks_start(start_date)
                end_date = line.date.date()
                if end_date < start_date:
                    start_date = datetime(
                        line.date.year - 1, 1, 1, 0, 0).date()
                    start_date = line.calculate_weeks_start(start_date)
                    end_date = datetime(
                        line.date.year, 1, 1, 0, 0).date()
                week = line.weeks_between(start_date, end_date)
                if week == 53:
                    week = 1
                line.date_week = week

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
            elif line.product_id and line.location_id and not line.lot_id:
                quant = self.env["stock.quant"].search([
                    ("product_id", "=", line.product_id.id),
                    ("location_id", "=", line.location_id.id)], limit=1)
                if quant:
                    line.rest = quant[:1].available_quantity

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
            quant = self.env["stock.quant"].search(
                [("location_id", "=", self.location_id.id),
                 ("product_id", "=", self.product_id.id),
                 ("batch_id", "=", self.batch_id.id)])
            lot = []
            for line in quant:
                if line.lot_id.id not in lot and line.lot_id.product_qty > 0:
                    lot.append(line.lot_id.id)
            domain = {"domain": {"lot_id": [("id", "in", lot)]}}
        return domain

    @api.onchange("batch_id")
    def onchange_batch_id(self):
        if self.product_id and (
            self.batch_id) and (
                self.picking_id.egg_production):
            if not self.picking_id.custom_date_done:
                raise ValidationError(
                    _("You must introduce the done date.")
                    )
            date_done = self.picking_id.custom_date_done.date()
            start_date = datetime(date_done.year, 1, 1, 0, 0).date()
            start_date = self.calculate_weeks_start(start_date)
            if date_done < start_date:
                start_date = datetime(
                    self.start_date.year - 1, 1, 1, 0, 0).date()
                start_date = self.calculate_weeks_start(start_date)
                date_done = datetime(
                    self.date_start.year, 1, 1, 0, 0).date()
            weeks = self.weeks_between(start_date, date_done)
            if weeks == 53:
                weeks = 1
            if weeks <= 9:
                weeks = u"0{}".format(weeks)
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

    @api.onchange('lot_id')
    def _onchange_lot_id(self):
        result = super(StockMoveLine, self)._onchange_lot_id()
        if self.lot_id:
            self.lot_id._compute_standard_price()
            self.standard_price = self.lot_id.standard_price
        return result

    @api.onchange("location_id", "location_dest_id")
    def _onchange_picking_id(self):
        if self.picking_id and self.picking_id.partner_id and (
            self.location_id.usage == "customer" or (
                self.location_dest_id.usage == "customer") or (
                    self.location_id.usage == "supplier") or (
                        self.location_dest_id.usage == "supplier")):
            self.owner_id = self.picking_id.partner_id.id

    # @api.onchange("qty_done", "rest")
    # def onchange_qty_done(self):
        # if self.picking_id and (
            # self.qty_done > self.rest) and (
                # self.location_id.usage == "internal"):
            # raise ValidationError(
                    # _("The done quantity can't be bigger than the rest.")
                    # )

    def weeks_between(self, start_date, end_date):
        weeks = rrule.rrule(rrule.WEEKLY, dtstart=start_date, until=end_date)
        return weeks.count()
