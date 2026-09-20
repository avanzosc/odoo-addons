# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, _
from odoo.exceptions import UserError
from datetime import timedelta
import pytz


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    picking_partner_id = fields.Many2one(
        string='Picking partner', comodel_name='res.partner', store=True,
        related='picking_id.partner_id')
    analytic_line_id = fields.Many2one(
        string='Analytic line', comodel_name='account.analytic.line')
    analytic_line_with_end_date = fields.Boolean(
        string='Analytic line with end date', default=False)

    def button_arrival(self):
        vals = self._catch_values_for_create_analytic_line()
        self.analytic_line_id = self.env['account.analytic.line'].create(
            vals).id

    def button_end(self):
        timezone = pytz.timezone(self._context.get('tz') or 'UTC')
        date_end = fields.Datetime.now()
        date_end = date_end.replace(tzinfo=pytz.timezone(
            'UTC')).astimezone(timezone)
        hours = int(date_end.strftime("%H"))
        minutes = int(date_end.strftime("%M"))
        stop = hours + minutes/60
        stop1 = timedelta(hours=stop)
        start = timedelta(hours=self.analytic_line_id.time_start)
        if stop1 > start:
            unit_amount = (stop1 - start).seconds / 3600
            vals = {'time_stop': round(stop, 14),
                    'unit_amount': unit_amount}
            self.analytic_line_id.write(vals)
            self.analytic_line_with_end_date = True

    def _catch_values_for_create_analytic_line(self):
        if not self.picking_id.project_id:
            raise UserError(
                _('The picking %s does not have a project defined') %
                (self.picking_id.name))
        cond = [('user_id', '=', self.env.user.id)]
        employee = self.env['hr.employee'].search(cond, limit=1)
        if not employee:
            raise UserError(
                _('No employee found for the user %s') %
                (self.env.user.name))
        timezone = pytz.timezone(self._context.get('tz') or 'UTC')
        date_start = fields.Datetime.now()
        date_start = date_start.replace(tzinfo=pytz.timezone(
            'UTC')).astimezone(timezone)
        hours = int(date_start.strftime("%H"))
        minutes = int(date_start.strftime("%M"))
        vals = {
            'name': _('Cage collected'),
            'account_id': self.picking_id.project_id.analytic_account_id.id,
            'employee_id': employee.id,
            'project_id': self.picking_id.project_id.id,
            'partner_id': self.picking_partner_id.id,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom_id.id,
            'date': date_start.date(),
            'time_start': round(hours + minutes/60, 14),
            'time_stop': round(hours + minutes/60, 14)
            }
        if self.picking_id.task_id:
            vals['task_id'] = self.picking_id.task_id.id
        return vals
