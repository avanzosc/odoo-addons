# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from dateutil import rrule
from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    def _default_entry_date(self):
        today = fields.Date.today()
        return today

    batch_type = fields.Selection(
        string="Batch Type", selection_add=[("breeding", "Breeding")]
    )
    description = fields.Text(string="Description")
    observation = fields.Text(string="Observation")
    entry_date = fields.Date(
        string="Entry date", default=lambda self: self._default_entry_date()
    )
    entry_week = fields.Integer(
        string="Entry Weeks", compute="_compute_entry_week", store=True
    )
    cleaned_date = fields.Date(string="Cleaned Date")
    cleaned_week = fields.Integer(
        string="Cleaned Weeks", compute="_compute_cleaned_week", store=True
    )
    liquidation_date = fields.Date(string="Liquidation Date")
    liquidation_week = fields.Integer(
        string="Liquidation Week", compute="_compute_liquidation_week", store=True
    )
    billing_date = fields.Date(string="Billing Date")
    billing_week = fields.Integer(
        string="Billing Weeks", compute="_compute_billing_week", store=True
    )
    feed_family = fields.Many2one(string="Feed Family", comodel_name="breeding.feed")
    picking_ids = fields.One2many(
        string="Transfers",
        domain="['|', ('location_id', '=', location_id), ('location_dest_id', '=', location_id)]",
    )
    state = fields.Selection(default="draft")
    lineage_percentage_ids = fields.One2many(
        string="Lineage Percentage",
        comodel_name="lineage.percentage",
        inverse_name="batch_id",
    )
    estimate_weight_ids = fields.One2many(
        string="Estimate Weight",
        comodel_name="estimate.weight",
        inverse_name="batch_id",
    )
    seq_name = fields.Char(string="Sequence Name")
    mother_lineage_ids = fields.One2many(
        string="Mother Lineage Relation",
        comodel_name="mother.lineage.relation",
        inverse_name="breeding_id",
    )
    farm_type = fields.Selection(
        string="Farm Type", related="warehouse_id.farm_type", store=True
    )

    @api.depends("entry_date")
    def _compute_entry_week(self):
        for batch in self:
            batch.entry_week = 0
            if batch.entry_date:
                start_date = datetime(batch.entry_date.year, 1, 1, 0, 0).date()
                start_date = batch.calculate_weeks_start(start_date)
                end_date = batch.entry_date
                if end_date < start_date:
                    start_date = datetime(batch.entry_date.year - 1, 1, 1, 0, 0).date()
                    start_date = batch.calculate_weeks_start(start_date)
                    end_date = datetime(batch.entry_date.year, 1, 1, 0, 0).date()
                week = batch.weeks_between(start_date, end_date)
                if week == 53:
                    week = 1
                batch.entry_week = week

    @api.depends("cleaned_date")
    def _compute_cleaned_week(self):
        for batch in self:
            batch.cleaned_week = 0
            if batch.cleaned_date:
                start_date = datetime(batch.cleaned_date.year, 1, 1, 0, 0).date()
                start_date = batch.calculate_weeks_start(start_date)
                end_date = batch.cleaned_date
                if end_date < start_date:
                    start_date = datetime(
                        batch.cleaned_date.year - 1, 1, 1, 0, 0
                    ).date()
                    start_date = batch.calculate_weeks_start(start_date)
                    end_date = datetime(batch.cleaned_date.year, 1, 1, 0, 0).date()
                week = batch.weeks_between(start_date, end_date)
                if week == 53:
                    week = 1
                batch.cleaned_week = week

    @api.depends("liquidation_date")
    def _compute_liquidation_week(self):
        for batch in self:
            batch.liquidation_week = 0
            if batch.liquidation_date:
                start_date = datetime(batch.liquidation_date.year, 1, 1, 0, 0).date()
                start_date = batch.calculate_weeks_start(start_date)
                end_date = batch.liquidation_date
                if end_date < start_date:
                    start_date = datetime(
                        batch.liquidation_date.year - 1, 1, 1, 0, 0
                    ).date()
                    start_date = batch.calculate_weeks_start(start_date)
                    end_date = datetime(batch.liquidation_date.year, 1, 1, 0, 0).date()
                week = batch.weeks_between(start_date, end_date)
                if week == 53:
                    week = 1
                batch.liquidation_week = week

    @api.depends("billing_date")
    def _compute_billing_week(self):
        for batch in self:
            batch.billing_week = 0
            if batch.billing_date:
                start_date = datetime(batch.billing_date.year, 1, 1, 0, 0).date()
                start_date = batch.calculate_weeks_start(start_date)
                end_date = batch.billing_date
                if end_date < start_date:
                    start_date = datetime(
                        batch.billing_date.year - 1, 1, 1, 0, 0
                    ).date()
                    start_date = batch.calculate_weeks_start(start_date)
                    end_date = datetime(batch.billing_date.year, 1, 1, 0, 0).date()
                week = batch.weeks_between(start_date, end_date)
                if week == 53:
                    week = 1
                batch.billing_week = week

    def weeks_between(self, start_date, end_date):
        weeks = rrule.rrule(rrule.WEEKLY, dtstart=start_date, until=end_date)
        return weeks.count()

    @api.onchange("location_id")
    def onchange_location_id(self):
        self.ensure_one()
        if self.location_id and self.batch_type == "breeding":
            self.name = self.location_id.name

    @api.onchange("stage_id")
    def onchange_stage_id(self):
        if (self.stage_id.id) == (
            self.env.ref("stock_picking_batch_breeding.batch_stage4").id
        ):
            self.cleaned_date = fields.Date.today()
        if (self.stage_id.id) == (
            self.env.ref("stock_picking_batch_breeding.batch_stage5").id
        ):
            self.liquidation_date = fields.Date.today()
        if (self.stage_id.id) == (
            self.env.ref("stock_picking_batch_breeding.batch_stage6").id
        ):
            self.billing_date = fields.Date.today()

    def _sanity_check(self):
        for batch in self:
            if batch.batch_type not in ("other"):
                return True
            else:
                return super()._sanity_check()

    @api.constrains("lineage_percentage_ids", "lineage_percentage_ids.percentage")
    def _check_lineage_percentage(self):
        for batch in self:
            if batch.lineage_percentage_ids:
                if sum(batch.lineage_percentage_ids.mapped("percentage")) != 100:
                    raise ValidationError(_("The sum of the percentages is not 100."))

    def action_calculate_lineage_percentage(self):
        self.ensure_one()
        if self.lineage_percentage_ids:
            for line in self.lineage_percentage_ids:
                line.unlink()
        if self.batch_type == "breeding" and self.move_line_ids:
            lineage = []
            lines = self.move_line_ids.filtered(
                lambda c: c.location_dest_id == self.location_id
                and (c.product_id.one_day_chicken)
                and c.lineage_id
            )
            if not lines:
                raise ValidationError(
                    _(
                        "No line has been found for the purchase of chicks "
                        + "with lineage."
                    )
                )
            if lines:
                total_qty = sum(lines.mapped("qty_done"))
                lineage_percentages = []
                for ml in lines:
                    if ml.lineage_id not in lineage and total_qty != 0:
                        lineage.append(ml.lineage_id)
                        lineage_qty = sum(
                            lines.filtered(
                                lambda c: c.lineage_id == (ml.lineage_id)
                            ).mapped("qty_done")
                        )
                        lineage_percentages.append(
                            [
                                0,
                                0,
                                {
                                    "lineage_id": ml.lineage_id.id,
                                    "percentage": lineage_qty * 100 / total_qty,
                                },
                            ]
                        )
                self.lineage_percentage_ids = lineage_percentages

    def action_calculate_mother_lineage_relation(self):
        self.ensure_one()
        if self.mother_lineage_ids:
            for line in self.mother_lineage_ids:
                line.unlink()
        if self.batch_type == "breeding" and self.move_line_ids:
            mother = []
            lines = self.move_line_ids.filtered(
                lambda c: c.location_dest_id == self.location_id
                and (c.product_id.one_day_chicken)
                and c.lot_id.batch_id
            )
            if not lines:
                raise ValidationError(
                    _(
                        "No line has been found for the purchase of chicks "
                        + "with mother."
                    )
                )
            if lines:
                total_qty = sum(lines.mapped("qty_done"))
                mother_percentages = []
                for ml in lines:
                    if ml.lot_id.batch_id not in mother and total_qty != 0:
                        mother.append(ml.lot_id.batch_id)
                        mother_qty = sum(
                            lines.filtered(
                                lambda c: c.lot_id.batch_id == (ml.lot_id.batch_id)
                            ).mapped("qty_done")
                        )
                        mother_percentages.append(
                            [
                                0,
                                0,
                                {
                                    "mother_id": ml.lot_id.batch_id.id,
                                    "percentage": mother_qty * 100 / total_qty,
                                },
                            ]
                        )
                self.mother_lineage_ids = mother_percentages

    def action_load_growth_rates(self):
        self.ensure_one()
        if not self.entry_date:
            raise ValidationError(_("You must introduce the entry date."))
        if self.estimate_weight_ids:
            for line in self.estimate_weight_ids:
                if line.real_weight or line.casualties:
                    raise ValidationError(
                        _(
                            "Cannot be upgraded as there is at least one "
                            + "real weight o casualties."
                        )
                    )
                else:
                    line.unlink()
        self.action_calculate_lineage_percentage()
        self.action_calculate_mother_lineage_relation()
        print("action calculate lineage percentage")
        if not self.lineage_percentage_ids:
            raise ValidationError(_("You must introduce the lineage percentages."))
        for lineage in self.lineage_percentage_ids:
            if not lineage.lineage_id.growth_rate_ids:
                raise ValidationError(
                    _("The lineage %s has no growth rates") % (lineage.lineage_id.name)
                )
        for line in self.lineage_percentage_ids[:1].lineage_id.growth_rate_ids:
            weight = []
            day = line.day
            for lineage in self.lineage_percentage_ids:
                percentage = lineage.percentage
                search_day = lineage.lineage_id.growth_rate_ids.filtered(
                    lambda c: c.day == day
                )
                if search_day:
                    weight.append(search_day.weight * 0.01 * percentage)
            if len(weight) == len(self.lineage_percentage_ids):
                weight = sum(weight)
                unit = sum(
                    self.move_line_ids.filtered(
                        lambda c: c.product_id.one_day_chicken
                        and (c.state == "done")
                        and (c.location_dest_id == self.location_id)
                    ).mapped("qty_done")
                ) - sum(
                    self.move_line_ids.filtered(
                        lambda c: (c.product_id.one_day_chicken)
                        and (c.state == "done")
                        and (c.location_id == (self.location_id))
                    ).mapped("qty_done")
                )
                self.estimate_weight_ids = [
                    (
                        0,
                        0,
                        {
                            "day": day,
                            "unit": unit,
                            "estimate_weight": weight,
                            "estimate_week_weight": weight,
                            "weight_uom_id": line.weight_uom_id.id,
                            "product_id": line.product_id.id,
                            "date": self.entry_date + relativedelta(days=day),
                        },
                    )
                ]
            else:
                raise ValidationError(
                    _("missing data for day %s of some lineage.") % (day)
                )

    def write(self, vals):
        stage_active = self.env.ref("stock_warehouse_farm.batch_stage2")
        for line in self:
            if (
                "stage_id" in vals
                and (vals["stage_id"] == stage_active.id)
                and (line.batch_type == "breeding")
            ):
                vals.update(
                    {
                        "name": self.env["ir.sequence"].next_by_code(
                            "stock.picking.batch"
                        )
                        or (line.location_id.name)
                    }
                )
        result = super().write(vals)
        return result
