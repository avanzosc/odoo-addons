# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import datetime, timedelta

from dateutil import rrule

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CancellationLine(models.Model):
    _name = "cancellation.line"
    _description = "Cancellation Line"

    batch_id = fields.Many2one(string="Mother", comodel_name="stock.picking.batch")
    week = fields.Integer(string="Week", compute="_compute_week", store=True)
    date = fields.Date(string="Date")
    product_id = fields.Many2one(string="Product", comodel_name="product.product")
    lot_id = fields.Many2one(
        string="Lot/Serial Number", comodel_name="stock.production.lot"
    )
    cancellation_qty = fields.Integer(string="Cancellations")
    inventory_qty = fields.Integer(
        string="Inventory", compute="_compute_inventory_qty", store=True
    )
    location_id = fields.Many2one(
        string="Location",
        comodel_name="stock.location",
        related="batch_id.location_id",
        store=True,
    )
    picking_id = fields.Many2one(string="Picking", comodel_name="stock.picking")
    move_line_id = fields.Many2one(string="Move Lines", comodel_name="stock.move.line")
    qty_done = fields.Float(
        string="Cancellation Done", related="move_line_id.qty_done", store=True
    )
    hen_life_week = fields.Integer(
        string="Hen Life", compute="_compute_hen_life", store=True
    )

    @api.depends("qty_done")
    def _compute_inventory_qty(self):
        for line in self:
            line.inventory_qty = 0
            stock_quant = self.env["stock.quant"].search(
                [
                    ("location_id", "=", self.location_id.id),
                    ("product_id", "=", self.lot_id.product_id.id),
                    ("lot_id", "=", self.lot_id.id),
                ],
                limit=1,
            )
            if stock_quant:
                line.inventory_qty = stock_quant.available_quantity

    @api.depends("date", "batch_id", "batch_id.start_date")
    def _compute_hen_life(self):
        for line in self:
            line.hen_life_week = 0
            if not line.batch_id and line.batch_id.start_date:
                raise ValidationError(_("The mother does not have a start date."))
            elif line.date and line.batch_id and line.batch_id.start_date:
                start_date = line.batch_id.start_date
                end_date = line.date
                if end_date < start_date:
                    raise ValidationError(
                        _("The date is prior to the mother's start date.")
                    )
                line.hen_life_week = line.weeks_between(start_date, end_date)

    @api.depends("date")
    def _compute_week(self):
        for line in self:
            line.week = 0
            if line.date:
                start_date = datetime(line.date.year, 1, 1, 0, 0).date()
                start_date = line.calculate_weeks_start(start_date)
                end_date = line.date
                if end_date < start_date:
                    start_date = datetime(line.date.year - 1, 1, 1, 0, 0).date()
                    start_date = line.calculate_weeks_start(start_date)
                    end_date = datetime(line.date.year, 1, 1, 0, 0).date()
                week = line.weeks_between(start_date, end_date)
                if week == 53:
                    week = 1
                line.week = week

    def calculate_weeks_start(self, start_date):
        self.ensure_one()
        weekday = start_date.weekday()
        if weekday <= 3:
            return start_date - timedelta(days=weekday)
        else:
            return start_date + timedelta(days=(7 - weekday))

    def weeks_between(self, start_date, end_date):
        weeks = rrule.rrule(rrule.WEEKLY, dtstart=start_date, until=end_date)
        return weeks.count()

    def button_do_cancellation(self):
        self.ensure_one()
        location_dest = self.env["stock.location"].search(
            [("usage", "=", "inventory"), ("scrap_location", "=", True)], limit=1
        )
        if not location_dest:
            raise ValidationError(
                _(
                    "No destination location has been found that is loss "
                    + "of inventory and scrap location."
                )
            )
        else:
            picking_type = self.env["stock.picking.type"].search(
                [
                    ("default_location_src_id", "=", self.location_id.id),
                    ("default_location_dest_id", "=", location_dest.id),
                ],
                limit=1,
            )
            if not picking_type:
                raise ValidationError(
                    _(
                        "No picking type has been found with source "
                        + "location {} and destination location {}."
                    ).format(self.location_id.name, location_dest.name)
                )
            if self.cancellation_qty != 0:
                picking = self.env["stock.picking"].create(
                    {
                        "picking_type_id": picking_type.id,
                        "location_id": self.location_id.id,
                        "location_dest_id": location_dest.id,
                        "batch_id": self.batch_id.id,
                        "custom_date_done": self.date,
                        "move_line_ids_without_package": [
                            (
                                0,
                                0,
                                {
                                    "product_id": self.product_id.id,
                                    "product_uom_id": self.product_id.uom_id.id,
                                    "lot_id": self.lot_id.id,
                                    "location_id": self.location_id.id,
                                    "location_dest_id": location_dest.id,
                                    "qty_done": self.cancellation_qty,
                                },
                            )
                        ],
                    }
                )
                picking.action_confirm()
                picking.button_validate()
                qty = 0
                stock_quant = self.env["stock.quant"].search(
                    [
                        ("location_id", "=", self.location_id.id),
                        ("product_id", "=", self.lot_id.product_id.id),
                        ("lot_id", "=", self.lot_id.id),
                    ],
                    limit=1,
                )
                if stock_quant:
                    qty = stock_quant.available_quantity
                self.write(
                    {
                        "picking_id": picking.id,
                        "inventory_qty": qty,
                        "move_line_id": (picking.move_line_ids_without_package[:1].id),
                    }
                )

    @api.onchange("batch_id")
    def onchange_batch_id(self):
        domain = {}
        self.ensure_one()
        if self.batch_id:
            products = []
            for line in self.batch_id.move_line_ids:
                products.append(line.product_id.id)
            if not products:
                raise ValidationError(_("There is no movement with products."))
            if products:
                domain = {"domain": {"product_id": [("id", "in", products)]}}
                if len(products) == 1:
                    self.product_id = products[0]
        return domain

    @api.onchange("product_id")
    def onchange_product_id(self):
        domain = {}
        self.ensure_one()
        if self.product_id:
            move_lines = self.batch_id.move_line_ids.filtered(
                lambda c: c.product_id == self.product_id
            )
            lots = []
            for line in move_lines:
                lots.append(line.lot_id.id)
            if not lots:
                raise ValidationError(_("There is no movement with mothers and lots."))
            if lots:
                domain = {"domain": {"lot_id": [("id", "in", lots)]}}
                if len(lots) == 1:
                    self.lot_id = lots[0]
        return domain
