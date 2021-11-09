# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    estimate_hour = fields.Float(
        string='Estimated Hours', compute='_compute_estimate_hour')
    limit_hour = fields.Float(
        string='Limit hour', compute='_compute_limit_hour')
    hour_type1 = fields.Float(
        string='Hours GX', compute='_compute_hours_type1')
    hour_type2 = fields.Float(
        string='Hours GF', compute='_compute_hours_type2')
    hour_type3 = fields.Float(
        string='Hours GC', compute='_compute_hours_type3')
    hour_type4 = fields.Float(
        string='Hours KC', compute='_compute_hours_type4')

    @api.depends('move_id.start_date_period', 'move_id.end_date_period',
                 'sale_line_ids')
    def _compute_estimate_hour(self):
        for line in self:
            duration = 0.0
            if line.sale_line_ids:
                analytic = line.env['account.analytic.line'].search(
                    [('so_line', '=', line.sale_line_ids.id)])
                for lines in analytic:
                    if (
                        lines.date > line.move_id.start_date_period) and (
                            lines.date < line.move_id.end_date_period):
                        duration += lines.unit_amount
            line.estimate_hour = duration

    @api.depends('move_id.start_date_period', 'move_id.end_date_period',
                 'sale_line_ids')
    def _compute_hours_type1(self):
        for line in self:
            duration = 0.0
            if line.sale_line_ids:
                type1 = self.env.ref('event_track_cancel_reason.time_type1').id
                analytic = line.env['account.analytic.line'].search(
                    [('so_line', '=', line.sale_line_ids.id), (
                        'time_type_id', '=', type1)])
                for lines in analytic:
                    if (
                        lines.date > line.move_id.start_date_period) and (
                            lines.date < line.move_id.end_date_period):
                        duration += lines.unit_amount
            line.hour_type1 = duration

    @api.depends('move_id.start_date_period', 'move_id.end_date_period',
                 'sale_line_ids')
    def _compute_hours_type2(self):
        for line in self:
            duration = 0.0
            if line.sale_line_ids:
                type2 = self.env.ref('event_track_cancel_reason.time_type2').id
                analytic = line.env['account.analytic.line'].search(
                    [('so_line', '=', line.sale_line_ids.id), (
                        'time_type_id', '=', type2)])
                for lines in analytic:
                    if (
                        lines.date > line.move_id.start_date_period) and (
                            lines.date < line.move_id.end_date_period):
                        duration += lines.unit_amount
            line.hour_type2 = duration

    @api.depends('move_id.start_date_period', 'move_id.end_date_period',
                 'sale_line_ids')
    def _compute_hours_type3(self):
        for line in self:
            duration = 0.0
            if line.sale_line_ids:
                type3 = self.env.ref('event_track_cancel_reason.time_type3').id
                analytic = line.env['account.analytic.line'].search(
                    [('so_line', '=', line.sale_line_ids.id), (
                        'time_type_id', '=', type3)])
                for lines in analytic:
                    if (
                        lines.date > line.move_id.start_date_period) and (
                            lines.date < line.move_id.end_date_period):
                        duration += lines.unit_amount
            line.hour_type3 = duration

    @api.depends('move_id.start_date_period', 'move_id.end_date_period',
                 'sale_line_ids')
    def _compute_hours_type4(self):
        for line in self:
            duration = 0.0
            if line.sale_line_ids:
                type4 = self.env.ref('event_track_cancel_reason.time_type4').id
                analytic = line.env['account.analytic.line'].search(
                    [('so_line', '=', line.sale_line_ids.id), (
                        'time_type_id', '=', type4)])
                for lines in analytic:
                    if (
                        lines.date > line.move_id.start_date_period) and (
                            lines.date < line.move_id.end_date_period):
                        duration += lines.unit_amount
            line.hour_type4 = duration

    @api.depends('estimate_hour', 'hour_type4')
    def _compute_limit_hour(self):
        for line in self:
            if line.estimate_hour:
                line.limit_hour = 0.85 * (line.estimate_hour - line.hour_type4)

    @api.onchange('limit_hour', 'estimate_hour', 'hour_type1', 'hour_type2', 'hour_type3', 'hour_type4')
    def onchange_quantity(self):
        if self.limit_hour > self.hour_type1 + self.hour_type2:
            self.quantity = self.limit_hour
        else:
            self.quantity = self.hour_type1 + self.hour_type2
