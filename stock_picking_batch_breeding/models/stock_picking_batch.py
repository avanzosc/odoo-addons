# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from datetime import datetime
from dateutil import rrule
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    def _default_entry_date(self):
        today = fields.Date.today()
        return today

    batch_type = fields.Selection(
        string='Batch Type',
        selection_add=[("breeding", "Breeding")])
    description = fields.Text(
        string='Description')
    observation = fields.Text(
        string='Observation')
    entry_date = fields.Date(
        string='Entry date',
        default=lambda self: self._default_entry_date())
    entry_week = fields.Integer(
        string='Entry Weeks',
        compute='_compute_entry_week',
        store=True)
    cleaned_date = fields.Date(
        string='Cleaned Date')
    cleaned_week = fields.Integer(
        string='Cleaned Weeks',
        compute='_compute_cleaned_week',
        store=True)
    liquidation_date = fields.Date(
        string='Liquidation Date')
    liquidation_week = fields.Integer(
        string='Liquidation Week',
        compute='_compute_liquidation_week',
        store=True)
    billing_date = fields.Date(
        string='Billing Date')
    billing_week = fields.Integer(
        string='Billing Weeks',
        compute='_compute_billing_week',
        store=True)
    feed_family = fields.Many2one(
        string='Feed Family',
        comodel_name='breeding.feed')
    picking_ids = fields.One2many(
        string='Transfers',
        domain="['|', ('location_id', '=', location_id), ('location_dest_id', '=', location_id)]")
    state = fields.Selection(default='draft')
    lineage_percentage_ids = fields.One2many(
        string="Lineage Percentage",
        comodel_name="lineage.percentage",
        inverse_name="batch_id")
    estimate_weight_ids = fields.One2many(
        string="Estimate Weight",
        comodel_name="estimate.weight",
        inverse_name="batch_id")
    age = fields.Integer(string="Age")

    @api.depends('entry_date')
    def _compute_entry_week(self):
        for batch in self:
            batch.entry_week = 0
            if batch.entry_date:
                start_date = datetime(batch.entry_date.year, 1, 1, 0, 0)
                end_date = batch.entry_date
                batch.entry_week = (
                    batch.weeks_between(start_date, end_date))

    @api.depends('cleaned_date')
    def _compute_cleaned_week(self):
        for batch in self:
            batch.cleaned_week = 0
            if batch.cleaned_date:
                start_date = datetime(batch.cleaned_date.year, 1, 1, 0, 0)
                end_date = batch.cleaned_date
                batch.cleaned_week = (
                    batch.weeks_between(start_date, end_date))

    @api.depends('liquidation_date')
    def _compute_liquidation_week(self):
        for batch in self:
            batch.liquidation_week = 0
            if batch.liquidation_date:
                start_date = datetime(batch.liquidation_date.year, 1, 1, 0, 0)
                end_date = batch.liquidation_date
                batch.liquidation_week = (
                    batch.weeks_between(start_date, end_date))

    @api.depends('billing_date')
    def _compute_billing_week(self):
        for batch in self:
            batch.billing_week = 0
            if batch.billing_date:
                start_date = datetime(batch.billing_date.year, 1, 1, 0, 0)
                end_date = batch.billing_date
                batch.billing_week = (
                    batch.weeks_between(start_date, end_date))

    def weeks_between(self, start_date, end_date):
        weeks = rrule.rrule(rrule.WEEKLY, dtstart=start_date, until=end_date)
        return weeks.count()

    @api.onchange("stage_id")
    def onchange_stage_id(self):
        if self.stage_id.id == 4:
            self.cleaned_date = fields.Date.today()
        if self.stage_id.id == 5:
            self.liquidation_date = fields.Date.today()
        if self.stage_id.id == 6:
            self.billing_date = fields.Date.today()

    def _sanity_check(self):
        for batch in self:
            if batch.batch_type not in ('other'):
                return True
            else:
                return super(StockPickingBatch, self)._sanity_check()

    @api.constrains(
        'lineage_percentage_ids', 'lineage_percentage_ids.percentage')
    def _check_lineage_percentage(self):
        for batch in self:
            if batch.lineage_percentage_ids:
                if sum(
                    batch.lineage_percentage_ids.mapped(
                        "percentage")) != 100:
                    raise ValidationError(
                        _("The sum of the percentages is not 100."))

    def action_load_growth_rates(self):
        self.ensure_one()
        if not self.entry_date:
            raise ValidationError(
                _("You must introduce the entry date."))
        if self.estimate_weight_ids:
            for line in self.estimate_weight_ids:
                if line.real_weight:
                    raise ValidationError(
                        _("Cannot be upgraded as there is at least one real weight"))
                else:
                    line.unlink()
        if not self.lineage_percentage_ids:
            raise ValidationError(
                _("You must introduce the lineage percentages."))
        for lineage in self.lineage_percentage_ids:
            if not lineage.lineage_id.growth_rate_ids:
                raise ValidationError(
                    _("The lineage %s has no growth rates") % (
                        lineage.lineage_id.name))
        for line in self.lineage_percentage_ids[:1].lineage_id.growth_rate_ids:
            weight = []
            day = line.day
            for lineage in self.lineage_percentage_ids:
                percentage = lineage.percentage
                search_day = lineage.lineage_id.growth_rate_ids.filtered(
                    lambda c: c.day == day)
                if search_day:
                    weight.append(search_day.weight * 0.01 * percentage)
            if len(weight) == len(self.lineage_percentage_ids):
                weight = sum(weight)
                self.estimate_weight_ids = [(0, 0, {
                    "day": day,
                    "estimate_weight": weight,
                    "weight_uom_id": line.weight_uom_id.id,
                    "product_id": line.product_id.id,
                    "date": self.entry_date + relativedelta(days=day)})]
