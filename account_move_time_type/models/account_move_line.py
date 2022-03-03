# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    estimate_hour = fields.Float(
        string='Estimated Hours', compute='_compute_estimate_hour',
        store=True)
    limit_hour = fields.Float(
        string='Limit hour', compute='_compute_estimate_hour', store=True)
    hour_type1 = fields.Float(
        string='Hours GX', compute='_compute_estimate_hour', store=True)
    hour_type2 = fields.Float(
        string='Hours GF', compute='_compute_estimate_hour', store=True)
    hour_type3 = fields.Float(
        string='Hours GC', compute='_compute_estimate_hour', store=True)
    hour_type4 = fields.Float(
        string='Hours KC', compute='_compute_estimate_hour', store=True)
    quantity2 = fields.Float(
        string='Quantity', default=1.0, digits='Product Unit of Measure',
        compute='_compute_estimate_hour', store=True)
    calculated_quantity2 = fields.Boolean(
        string='Calculated_quantity2', compute='_compute_estimate_hour',
        store=True)

    @api.depends('move_id', 'move_id.timesheet_ids',
                 'move_id.timesheet_ids.time_type_id',
                 'move_id.timesheet_ids.unit_amount',
                 'move_id.timesheet_ids.amount',
                 'move_id.timesheet_ids.so_line', 'move_id.start_date_period',
                 'move_id.end_date_period', 'sale_line_ids')
    def _compute_estimate_hour(self):
        type1 = self.env.ref('event_track_cancel_reason.time_type1').id
        type2 = self.env.ref('event_track_cancel_reason.time_type2').id
        type3 = self.env.ref('event_track_cancel_reason.time_type3').id
        type4 = self.env.ref('event_track_cancel_reason.time_type4').id
        for line in self:
            calculated_quantity2 = False
            if not line.contract_line_id:
                timesheets = line.mapped('move_id.timesheet_ids').filtered(
                    lambda t: t.so_line in line.sale_line_ids)
                if (
                    line.move_id.start_date_period) and (
                        line.move_id.end_date_period):
                    timesheets = timesheets.filtered(
                        lambda x: x.date >= line.move_id.start_date_period and (
                            x.date <= line.move_id.end_date_period))
                line.estimate_hour = sum(timesheets.mapped('unit_amount'))
                line.hour_type1 = sum(timesheets.filtered(
                    lambda l: l.time_type_id.id == type1).mapped(
                        'unit_amount'))
                line.hour_type2 = sum(timesheets.filtered(
                    lambda l: l.time_type_id.id == type2).mapped(
                        'unit_amount'))
                line.hour_type3 = sum(timesheets.filtered(
                    lambda l: l.time_type_id.id == type3).mapped(
                        'unit_amount'))
                line.hour_type4 = sum(timesheets.filtered(
                    lambda l: l.time_type_id.id == type4).mapped(
                        'unit_amount'))
                line.quantity2 = line.hour_type1 + line.hour_type2
                line.limit_hour = 0.85 * (
                    line.estimate_hour - line.hour_type4)
                if line.limit_hour > line.quantity2:
                    line.quantity2 = line.limit_hour
                if line.quantity2 > 0 and line.quantity != line.quantity2:
                    calculated_quantity2 = True
                if ('<NewId' not in str(line) and line.quantity2 > 0 and
                        line.quantity != line.quantity2):
                    print ('entro en self.env.cr.execute')
                    self.env.cr.execute(
                        "UPDATE account_move_line SET quantity = %s WHERE id = %s;",
                        (line.quantity2, line.id,),)
            line.calculated_quantity2 = calculated_quantity2
