# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api
from datetime import datetime
from dateutil import rrule


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
        selection=[("mother", "Mother")])
    location_change_id = fields.Many2one(
        string='Location Change',
        comodel_name='stock.location')

    @api.depends('start_date')
    def _compute_start_weeks(self):
        for lot in self:
            lot.start_weeks = 0
            if lot.start_date:
                start_date = datetime(lot.start_date.year, 1, 1, 0, 0).date()
                end_date = lot.start_date
                lot.start_weeks = (
                    lot.weeks_between(start_date, end_date))

    @api.depends('start_laying_date')
    def _compute_start_laying_weeks(self):
        for lot in self:
            lot.start_laying_weeks = 0
            if lot.start_laying_date:
                start_date = datetime(
                    lot.start_laying_date.year, 1, 1, 0, 0).date()
                end_date = lot.start_laying_date
                lot.start_laying_weeks = (
                    lot.weeks_between(start_date, end_date))

    @api.depends('start_birth_date')
    def _compute_start_birth_weeks(self):
        for lot in self:
            lot.start_birth_weeks = 0
            if lot.start_birth_date:
                start_date = datetime(
                    lot.start_birth_date.year, 1, 1, 0, 0).date()
                end_date = lot.start_birth_date
                lot.start_birth_weeks = (
                    lot.weeks_between(start_date, end_date))

    @api.depends('change_house_date')
    def _compute_change_house_weeks(self):
        for lot in self:
            lot.change_house_weeks = 0
            if lot.change_house_date:
                start_date = datetime(
                    lot.change_house_date.year, 1, 1, 0, 0).date()
                end_date = lot.change_house_date
                lot.change_house_weeks = (
                    lot.weeks_between(start_date, end_date))

    @api.depends('end_rearing_date')
    def _compute_end_rearing_weeks(self):
        for lot in self:
            lot.end_rearing_weeks = 0
            if lot.end_rearing_date:
                start_date = datetime(
                    lot.end_rearing_date.year, 1, 1, 0, 0).date()
                end_date = lot.end_rearing_date
                lot.end_rearing_weeks = (
                    lot.weeks_between(start_date, end_date))

    @api.depends('end_laying_date')
    def _compute_end_laying_weeks(self):
        for lot in self:
            lot.end_laying_weeks = 0
            if lot.end_laying_date:
                start_date = datetime(
                    lot.end_laying_date.year, 1, 1, 0, 0).date()
                end_date = lot.end_laying_date
                lot.end_laying_weeks = (
                    lot.weeks_between(start_date, end_date))

    @api.depends('end_birth_date')
    def _compute_end_birth_weeks(self):
        for lot in self:
            lot.end_birth_weeks = 0
            if lot.end_birth_date:
                start_date = datetime(
                    lot.end_birth_date.year, 1, 1, 0, 0).date()
                end_date = lot.end_birth_date
                lot.end_birth_weeks = (
                    lot.weeks_between(start_date, end_date))

    @api.depends('closing_date')
    def _compute_closing_weeks(self):
        for lot in self:
            lot.closing_weeks = 0
            if lot.closing_date:
                start_date = datetime(
                    lot.closing_date.year, 1, 1, 0, 0).date()
                end_date = lot.closing_date
                lot.closing_weeks = (
                    lot.weeks_between(start_date, end_date))

    def weeks_between(self, start_date, end_date):
        weeks = rrule.rrule(rrule.WEEKLY, dtstart=start_date, until=end_date)
        return weeks.count()

    @api.onchange("location_change_id")
    def onchange_location_change(self):
        if self.location_change_id:
            self.change_house_date = fields.Date.today()

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
                        self.env['birth.rate'].create(vals)
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
                        self.env['laying.rate'].create(vals)
