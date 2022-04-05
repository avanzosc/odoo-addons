# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api, _
from datetime import datetime
from dateutil import rrule


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    def _default_stage_id(self):
        stage = self.env['picking.batch.stage'].search([('id', '=', '1')])
        return stage.id

    def _default_entry_date(self):
        today = fields.Date.today()
        return today

    lot_id = fields.Many2one(
        string='Mother',
        comodel_name='stock.production.lot',
        domain="[('product_id.categ_id.type_id','=', 1)]")
    description = fields.Text(
        string='Description')
    observation = fields.Text(
        string='Observation')
    location_id = fields.Many2one(
        string='Location',
        comodel_name='stock.location')
    warehouse_id = fields.Many2one(
        string='Farm',
        comodel_name='stock.warehouse',
        related='location_id.warehouse_id',
        store=True)
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
    picking_count = fields.Integer(
        '# Transfers',
        compute='_compute_picking_count')
    move_count = fields.Integer(
        '# Stock Moves',
        compute='_compute_move_count')
    move_line_count = fields.Integer(
        '# Stock Move Lines',
        compute='_compute_move_line_count')
    stage_id = fields.Many2one(
        string='Stage',
        comodel_name="picking.batch.stage",
        copy=False,
        default=lambda self: self._default_stage_id())

    def _compute_picking_count(self):
        for batch in self:
            batch.picking_count = len(batch.picking_ids)

    def _compute_move_count(self):
        for batch in self:
            batch.move_count = len(batch.move_ids)

    def _compute_move_line_count(self):
        for batch in self:
            batch.move_line_count = len(batch.move_line_ids)

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

    def action_view_picking(self):
        context = self.env.context.copy()
        context.update({'default_batch_id': self.id})
        if 'search_default_draft' in context:
            context.update({'search_default_draft': False})
        context.update({'group_by': 'picking_type_id'})
        return {
            'name': _("Transfers"),
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'domain': [('id', 'in', self.picking_ids.ids)],
            'type': 'ir.actions.act_window',
            'context': context
        }

    def action_view_move(self):
        context = self.env.context.copy()
        context.update({'default_batch_id': self.id})
        context.update({'group_by': 'picking_type_id'})
        return {
            'name': _("Stock Moves"),
            'view_mode': 'tree,form',
            'res_model': 'stock.move',
            'domain': [('id', 'in', self.move_ids.ids)],
            'type': 'ir.actions.act_window',
            'context': context
        }

    def action_view_move_line(self):
        context = self.env.context.copy()
        context.update({'default_batch_id': self.id})
        context.update({'group_by': 'picking_type_id'})
        return {
            'name': _("Stock Move Lines"),
            'view_mode': 'tree,form',
            'res_model': 'stock.move.line',
            'domain': [('id', 'in', self.move_line_ids.ids)],
            'type': 'ir.actions.act_window',
            'context': context
        }

    @api.onchange("stage_id")
    def onchange_stage_id(self):
        if self.stage_id.id == 2:
            self.cleaned_date = fields.Date.today()
        if self.stage_id.id == 3:
            self.liquidation_date = fields.Date.today()
        if self.stage_id.id == 4:
            self.billing_date = fields.Date.today()
