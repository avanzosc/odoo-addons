# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import datetime, timedelta

from dateutil import rrule
from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    name = fields.Char(string="Code")
    operating_number = fields.Char(string="Operating Number")
    lineage_id = fields.Many2one(string="Lineage", comodel_name="lineage")
    start_date = fields.Date(string="Start Date")
    start_weeks = fields.Integer(
        string="Weeks", compute="_compute_start_weeks", store=True
    )
    start_laying_date = fields.Date(string="Start Laying")
    start_laying_weeks = fields.Integer(
        string="Start Laying Weeks", compute="_compute_start_laying_weeks", store=True
    )
    start_birth_date = fields.Date(string="Start Birth")
    start_birth_weeks = fields.Integer(
        string="Birth Weeks", compute="_compute_start_birth_weeks", store=True
    )
    change_house_date = fields.Date(string="Change House")
    change_house_weeks = fields.Integer(
        string="Change House Weeks", compute="_compute_change_house_weeks", store=True
    )
    end_rearing_date = fields.Date(string="Rearing End")
    end_rearing_weeks = fields.Integer(
        string="Rearing End Weeks", compute="_compute_end_rearing_weeks", store=True
    )
    end_laying_date = fields.Date(string="End Laying")
    end_laying_weeks = fields.Integer(
        string="End Laying Weeks", compute="_compute_end_laying_weeks", store=True
    )
    end_birth_date = fields.Date(string="End Birth")
    end_birth_weeks = fields.Integer(
        string="End Weeks", compute="_compute_end_birth_weeks", store=True
    )
    closing_date = fields.Date(string="Closing")
    closing_weeks = fields.Integer(
        string="Closing Weeks", compute="_compute_closing_weeks", store=True
    )
    laying_correlation = fields.Float(string="% of Laying Correlation")
    birth_correlation = fields.Float(string="% of Birth Correlation")
    consumed_feed = fields.Float(string="Consumed Feed")
    birth_rate_ids = fields.One2many(
        string="Birth Rate", comodel_name="birth.rate", inverse_name="mother_id"
    )
    laying_rate_ids = fields.One2many(
        string="Laying Rate", comodel_name="laying.rate", inverse_name="mother_id"
    )
    batch_type = fields.Selection(
        string="Batch Type", selection_add=[("mother", "Mother")]
    )
    location_change_id = fields.Many2one(
        string="Rearing House", comodel_name="stock.location", copy=False
    )
    hen_unit = fields.Integer(
        string="Hen Units", compute="_compute_hen_unit", store=True
    )
    cancellation_line_ids = fields.One2many(
        string="Cancellations",
        comodel_name="cancellation.line",
        inverse_name="batch_id",
    )

    @api.depends("picking_ids", "picking_ids.state")
    def _compute_state(self):
        super()._compute_state()
        for batch in self:
            if not batch.picking_ids:
                batch.state = "draft"

    @api.constrains("name")
    def _check_name(self):
        for batch in self:
            same = self.env["stock.picking.batch"].search(
                [("name", "=", batch.name), ("id", "!=", batch.id)]
            )
            if same:
                raise ValidationError(_("Mother/Breeding already exists."))

    @api.depends(
        "picking_ids",
        "picking_ids.state",
        "move_line_ids",
        "move_line_ids.qty_done",
        "move_line_ids.product_id",
        "move_line_ids.product_id.is_hen",
    )
    def _compute_hen_unit(self):
        for batch in self:
            batch.hen_unit = 0
            if batch.move_line_ids and batch.batch_type == "mother":
                in_qty = sum(
                    batch.move_line_ids.filtered(
                        lambda c: c.state == "done"
                        and c.product_id.is_hen
                        and (c.location_dest_id == batch.location_id)
                    ).mapped("qty_done")
                )
                out_qty = sum(
                    batch.move_line_ids.filtered(
                        lambda c: c.state == "done"
                        and c.product_id.is_hen is (True)
                        and c.location_id == batch.location_id
                    ).mapped("qty_done")
                )
                batch.hen_unit = in_qty - out_qty

    def calculate_weeks_start(self, start_date):
        self.ensure_one()
        weekday = start_date.weekday()
        if weekday <= 3:
            return start_date - timedelta(days=weekday)
        else:
            return start_date + timedelta(days=(7 - weekday))

    @api.depends("start_date")
    def _compute_start_weeks(self):
        for batch in self:
            batch.start_weeks = 0
            if batch.start_date:
                start_date = datetime(batch.start_date.year, 1, 1, 0, 0).date()
                start_date = batch.calculate_weeks_start(start_date)
                end_date = batch.start_date
                if end_date < start_date:
                    start_date = datetime(batch.start_date.year - 1, 1, 1, 0, 0).date()
                    start_date = batch.calculate_weeks_start(start_date)
                    end_date = datetime(batch.start_date.year, 1, 1, 0, 0).date()
                week = batch.weeks_between(start_date, end_date)
                if week == 53:
                    week = 1
                batch.start_weeks = week

    @api.depends("start_laying_date")
    def _compute_start_laying_weeks(self):
        for batch in self:
            batch.start_laying_weeks = 0
            if batch.start_laying_date:
                start_date = datetime(batch.start_laying_date.year, 1, 1, 0, 0).date()
                start_date = batch.calculate_weeks_start(start_date)
                end_date = batch.start_laying_date
                if end_date < start_date:
                    start_date = datetime(
                        batch.start_laying_date.year - 1, 1, 1, 0, 0
                    ).date()
                    start_date = batch.calculate_weeks_start(start_date)
                    end_date = datetime(batch.start_laying_date.year, 1, 1, 0, 0).date()
                week = batch.weeks_between(start_date, end_date)
                if week == 53:
                    week = 1
                batch.start_laying_weeks = week

    @api.depends("start_birth_date")
    def _compute_start_birth_weeks(self):
        for batch in self:
            batch.start_birth_weeks = 0
            if batch.start_birth_date:
                start_date = datetime(batch.start_birth_date.year, 1, 1, 0, 0).date()
                start_date = batch.calculate_weeks_start(start_date)
                end_date = batch.start_birth_date
                if end_date < start_date:
                    start_date = datetime(
                        batch.start_birth_date.year - 1, 1, 1, 0, 0
                    ).date()
                    start_date = batch.calculate_weeks_start(start_date)
                    end_date = datetime(batch.start_birth_date.year, 1, 1, 0, 0).date()
                week = batch.weeks_between(start_date, end_date)
                if week == 53:
                    week = 1
                batch.start_birth_weeks = week

    @api.depends("change_house_date")
    def _compute_change_house_weeks(self):
        for batch in self:
            batch.change_house_weeks = 0
            if batch.change_house_date:
                start_date = datetime(batch.change_house_date.year, 1, 1, 0, 0).date()
                start_date = batch.calculate_weeks_start(start_date)
                end_date = batch.change_house_date
                if end_date < start_date:
                    start_date = datetime(
                        batch.change_house_date.year - 1, 1, 1, 0, 0
                    ).date()
                    start_date = batch.calculate_weeks_start(start_date)
                    end_date = datetime(batch.change_house_date.year, 1, 1, 0, 0).date()
                week = batch.weeks_between(start_date, end_date)
                if week == 53:
                    week = 1
                batch.change_house_weeks = week

    @api.depends("end_rearing_date")
    def _compute_end_rearing_weeks(self):
        for batch in self:
            batch.end_rearing_weeks = 0
            if batch.end_rearing_date:
                start_date = datetime(batch.end_rearing_date.year, 1, 1, 0, 0).date()
                start_date = batch.calculate_weeks_start(start_date)
                end_date = batch.end_rearing_date
                if end_date < start_date:
                    start_date = datetime(
                        batch.end_rearing_date.year - 1, 1, 1, 0, 0
                    ).date()
                    start_date = batch.calculate_weeks_start(start_date)
                    end_date = datetime(batch.end_rearing_date.year, 1, 1, 0, 0).date()
                week = batch.weeks_between(start_date, end_date)
                if week == 53:
                    week = 1
                batch.end_rearing_weeks = week

    @api.depends("end_laying_date")
    def _compute_end_laying_weeks(self):
        for batch in self:
            batch.end_laying_weeks = 0
            if batch.end_laying_date:
                start_date = datetime(batch.end_laying_date.year, 1, 1, 0, 0).date()
                start_date = batch.calculate_weeks_start(start_date)
                end_date = batch.end_laying_date
                if end_date < start_date:
                    start_date = datetime(
                        batch.end_laying_date.year - 1, 1, 1, 0, 0
                    ).date()
                    start_date = batch.calculate_weeks_start(start_date)
                    end_date = datetime(batch.end_laying_date.year, 1, 1, 0, 0).date()
                week = batch.weeks_between(start_date, end_date)
                if week == 53:
                    week = 1
                batch.end_laying_weeks = week

    @api.depends("end_birth_date")
    def _compute_end_birth_weeks(self):
        for batch in self:
            batch.end_birth_weeks = 0
            if batch.end_birth_date:
                start_date = datetime(batch.end_birth_date.year, 1, 1, 0, 0).date()
                start_date = batch.calculate_weeks_start(start_date)
                end_date = batch.end_birth_date
                if end_date < start_date:
                    start_date = datetime(
                        batch.end_birth_date.year - 1, 1, 1, 0, 0
                    ).date()
                    start_date = batch.calculate_weeks_start(start_date)
                    end_date = datetime(batch.end_birth_date.year, 1, 1, 0, 0).date()
                week = batch.weeks_between(start_date, end_date)
                if week == 53:
                    week = 1
                batch.end_birth_weeks = week

    @api.depends("closing_date")
    def _compute_closing_weeks(self):
        for batch in self:
            batch.closing_weeks = 0
            if batch.closing_date:
                start_date = datetime(batch.closing_date.year, 1, 1, 0, 0).date()
                start_date = batch.calculate_weeks_start(start_date)
                end_date = batch.closing_date
                if end_date < start_date:
                    start_date = datetime(
                        batch.closing_date.year - 1, 1, 1, 0, 0
                    ).date()
                    start_date = batch.calculate_weeks_start(start_date)
                    end_date = datetime(batch.closing_date.year, 1, 1, 0, 0).date()
                week = batch.weeks_between(start_date, end_date)
                if week == 53:
                    week = 1
                batch.closing_weeks = week

    def weeks_between(self, start_date, end_date):
        weeks = rrule.rrule(rrule.WEEKLY, dtstart=start_date, until=end_date)
        return weeks.count()

    @api.onchange("location_change_id")
    def onchange_location_change(self):
        if self.location_change_id:
            self.change_house_date = fields.Date.today()

    @api.onchange("start_laying_date")
    def onchange_start_laying_date(self):
        self.ensure_one()
        if self.start_laying_date:
            for line in self.laying_rate_ids:
                line.laying_start_date = self.start_laying_date + (
                    relativedelta(days=(line.week - 1) * 7)
                )

    @api.onchange("start_birth_date")
    def onchange_start_birth_date(self):
        self.ensure_one()
        if self.start_birth_date:
            for line in self.birth_rate_ids:
                line.birth_start_date = self.start_birth_date + (
                    relativedelta(days=(line.week - 1) * 7)
                )

    def action_copy_lineage_rates(self):
        self.ensure_one()
        if self.lineage_id:
            if self.lineage_id.birth_rate_ids:
                for rate in self.lineage_id.birth_rate_ids:
                    vals = {
                        "mother_id": self.id,
                        "week": rate.week,
                        "percentage_birth": rate.percentage_birth,
                    }
                    cond = [
                        ("mother_id", "=", vals["mother_id"]),
                        ("week", "=", vals["week"]),
                    ]
                    lines = self.env["birth.rate"].search(cond)
                    if not lines:
                        line = self.env["birth.rate"].create(vals)
                        if self.start_birth_date:
                            line.write(
                                {
                                    "birth_start_date": (
                                        self.start_birth_date
                                        + (relativedelta(days=(line.week - 1) * 7))
                                    )
                                }
                            )
            if self.lineage_id.laying_rate_ids:
                for rate in self.lineage_id.laying_rate_ids:
                    vals = {
                        "mother_id": self.id,
                        "week": rate.week,
                        "percentage_laying": rate.percentage_laying,
                    }
                    cond = [
                        ("mother_id", "=", vals["mother_id"]),
                        ("week", "=", vals["week"]),
                    ]
                    lines = self.env["laying.rate"].search(cond)
                    if not lines:
                        line = self.env["laying.rate"].create(vals)
                        if self.start_laying_date:
                            line.write(
                                {
                                    "laying_start_date": (
                                        self.start_laying_date
                                        + (relativedelta(days=(line.week - 1) * 7))
                                    )
                                }
                            )
