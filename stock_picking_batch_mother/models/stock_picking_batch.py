# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from datetime import datetime
from dateutil import rrule
from dateutil.relativedelta import relativedelta


class StockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'

    name = fields.Char(
        string='Code')
    operating_number = fields.Char(
        string='Operating Number')
    lineage_id = fields.Many2one(
        string='Lineage',
        comodel_name='lineage')
    start_date = fields.Date(
        string='Start Date')
    start_weeks = fields.Integer(
        string='Weeks',
        compute='_compute_start_weeks',
        store=True)
    start_laying_date = fields.Date(
        string='Start Laying')
    start_laying_weeks = fields.Integer(
        string='Start Laying Weeks',
        compute='_compute_start_laying_weeks',
        store=True)
    start_birth_date = fields.Date(
        string='Start Birth')
    start_birth_weeks = fields.Integer(
        string='Birth Weeks',
        compute='_compute_start_birth_weeks',
        store=True)
    change_house_date = fields.Date(
        string='Change House')
    change_house_weeks = fields.Integer(
        string='Change House Weeks',
        compute='_compute_change_house_weeks',
        store=True)
    end_rearing_date = fields.Date(
        string='End Rearing')
    end_rearing_weeks = fields.Integer(
        string='End Rearing Weeks',
        compute='_compute_end_rearing_weeks',
        store=True)
    end_laying_date = fields.Date(
        string='End Laying')
    end_laying_weeks = fields.Integer(
        string='End Laying Weeks',
        compute='_compute_end_laying_weeks',
        store=True)
    end_birth_date = fields.Date(
        string='End Birth')
    end_birth_weeks = fields.Integer(
        string='End Weeks',
        compute='_compute_end_birth_weeks',
        store=True)
    closing_date = fields.Date(
        string='Closing')
    closing_weeks = fields.Integer(
        string='Closing Weeks',
        compute='_compute_closing_weeks',
        store=True)
    laying_correlation = fields.Float(
        string='% of Laying Correlation')
    birth_correlation = fields.Float(
        string='% of Birth Correlation')
    consumed_feed = fields.Float(
        string='Consumed Feed')
    birth_rate_ids = fields.One2many(
        string='Birth Rate',
        comodel_name='birth.rate',
        inverse_name='mother_id')
    laying_rate_ids = fields.One2many(
        string='Laying Rate',
        comodel_name='laying.rate',
        inverse_name='mother_id')
    batch_type = fields.Selection(
        string='Batch Type',
        selection_add=[("mother", "Mother")])
    location_change_id = fields.Many2one(
        string='Location Change',
        comodel_name='stock.location')
    hen_unit = fields.Integer(
        string='Hen Units',
        compute="_compute_hen_unit",
        store=True)
    cancellation_line_ids = fields.One2many(
        string="Cancellations",
        comodel_name="cancellation.line",
        inverse_name="batch_id")

    @api.depends("location_id", "location_id.quant_ids",
                 "location_id.quant_ids.quantity")
    def _compute_hen_unit(self):
        for line in self:
            line.hen_unit = 0
            if line.location_id and line.location_id.quant_ids:
                quants = line.location_id.quant_ids.filtered(
                    lambda x: x.product_id.is_hen is True)
                line.hen_unit = sum(quants.mapped("quantity"))

    @api.depends('start_date')
    def _compute_start_weeks(self):
        for batch in self:
            batch.start_weeks = 0
            if batch.start_date:
                start_date = datetime(batch.start_date.year, 1, 1, 0, 0).date()
                end_date = batch.start_date
                batch.start_weeks = (
                    batch.weeks_between(start_date, end_date))

    @api.depends('start_laying_date')
    def _compute_start_laying_weeks(self):
        for batch in self:
            batch.start_laying_weeks = 0
            if batch.start_laying_date:
                start_date = datetime(
                    batch.start_laying_date.year, 1, 1, 0, 0).date()
                end_date = batch.start_laying_date
                batch.start_laying_weeks = (
                    batch.weeks_between(start_date, end_date))

    @api.depends('start_birth_date')
    def _compute_start_birth_weeks(self):
        for batch in self:
            batch.start_birth_weeks = 0
            if batch.start_birth_date:
                start_date = datetime(
                    batch.start_birth_date.year, 1, 1, 0, 0).date()
                end_date = batch.start_birth_date
                batch.start_birth_weeks = (
                    batch.weeks_between(start_date, end_date))

    @api.depends('change_house_date')
    def _compute_change_house_weeks(self):
        for batch in self:
            batch.change_house_weeks = 0
            if batch.change_house_date:
                start_date = datetime(
                    batch.change_house_date.year, 1, 1, 0, 0).date()
                end_date = batch.change_house_date
                batch.change_house_weeks = (
                    batch.weeks_between(start_date, end_date))

    @api.depends('end_rearing_date')
    def _compute_end_rearing_weeks(self):
        for batch in self:
            batch.end_rearing_weeks = 0
            if batch.end_rearing_date:
                start_date = datetime(
                    batch.end_rearing_date.year, 1, 1, 0, 0).date()
                end_date = batch.end_rearing_date
                batch.end_rearing_weeks = (
                    batch.weeks_between(start_date, end_date))

    @api.depends('end_laying_date')
    def _compute_end_laying_weeks(self):
        for batch in self:
            batch.end_laying_weeks = 0
            if batch.end_laying_date:
                start_date = datetime(
                    batch.end_laying_date.year, 1, 1, 0, 0).date()
                end_date = batch.end_laying_date
                batch.end_laying_weeks = (
                    batch.weeks_between(start_date, end_date))

    @api.depends('end_birth_date')
    def _compute_end_birth_weeks(self):
        for batch in self:
            batch.end_birth_weeks = 0
            if batch.end_birth_date:
                start_date = datetime(
                    batch.end_birth_date.year, 1, 1, 0, 0).date()
                end_date = batch.end_birth_date
                batch.end_birth_weeks = (
                    batch.weeks_between(start_date, end_date))

    @api.depends('closing_date')
    def _compute_closing_weeks(self):
        for batch in self:
            batch.closing_weeks = 0
            if batch.closing_date:
                start_date = datetime(
                    batch.closing_date.year, 1, 1, 0, 0).date()
                end_date = batch.closing_date
                batch.closing_weeks = (
                    batch.weeks_between(start_date, end_date))

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
                line.laying_start_date = (
                    self.start_laying_date + (
                        relativedelta(days=(line.week - 1) * 7)))
            for line in self.cancellation_line_ids:
                line.date = (
                    self.start_laying_date + (
                        relativedelta(days=(line.week - 1) * 7)))

    @api.onchange("start_birth_date")
    def onchange_start_birth_date(self):
        self.ensure_one()
        if self.start_birth_date:
            for line in self.birth_rate_ids:
                line.birth_start_date = (
                    self.start_birth_date + (
                        relativedelta(days=(line.week - 1) * 7)))

    def action_copy_lineage_rates(self):
        self.ensure_one()
        if self.lineage_id:
            if self.lineage_id.birth_rate_ids:
                for rate in self.lineage_id.birth_rate_ids:
                    vals = {'mother_id': self.id,
                            'week': rate.week,
                            'percentage_birth': rate.percentage_birth}
                    cond = [(
                        'mother_id', '=', vals['mother_id']), (
                            'week', '=', vals['week'])]
                    lines = self.env['birth.rate'].search(cond)
                    if not lines:
                        line = self.env['birth.rate'].create(vals)
                        if self.start_birth_date:
                            line.write({"birth_start_date": (
                                self.start_birth_date + (
                                    relativedelta(days=(line.week - 1) * 7)))})
            if self.lineage_id.laying_rate_ids:
                for rate in self.lineage_id.laying_rate_ids:
                    vals = {'mother_id': self.id,
                            'week': rate.week,
                            'percentage_laying': rate.percentage_laying}
                    cond = [(
                        'mother_id', '=', vals['mother_id']), (
                            'week', '=', vals['week'])]
                    lines = self.env['laying.rate'].search(cond)
                    if not lines:
                        line = self.env['laying.rate'].create(vals)
                        if self.start_laying_date:
                            line.write({"laying_start_date": (
                                self.start_laying_date + (
                                    relativedelta(days=(line.week - 1) * 7)))})

    def action_calculate_cancellations(self):
        self.ensure_one()
        if self.lineage_id.laying_rate_ids:
            for rate in self.lineage_id.laying_rate_ids:
                for line in self.move_line_ids:
                    cancel_vals = {"batch_id": self.id,
                                   "week": rate.week,
                                   "product_id": line.product_id.id,
                                   "lot_id": line.lot_id.id}
                    if self.start_laying_date:
                        cancel_vals.update({"date": (
                            self.start_laying_date + (
                                relativedelta(days=(rate.week - 1)*7)))})
                    cond = [("batch_id", "=", self.id),
                            ("week", "=", rate.week),
                            ("product_id", "=", line.product_id.id),
                            ("lot_id", "=", line.lot_id.id)]
                    cancel_lines = self.env["cancellation.line"].search(cond)
                    if not cancel_lines:
                        self.env["cancellation.line"].create(cancel_vals)
