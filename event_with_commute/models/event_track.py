# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, _
from odoo.exceptions import UserError


class EventTrack(models.Model):
    _inherit = 'event.track'

    def write(self, vals):
        res = super(EventTrack, self).write(vals)
        for track in self:
            if not track.partner_id:
                raise UserError(
                    _('You must define a speaker for the session : {}').format(
                        track.name))
            cond = [('partner_id', '=', track.partner_id.id)]
            user = self.env['res.users'].search(cond, limit=1)
            if not user:
                raise UserError(
                    _('User not found for speaker: {}').format(
                        track.partner_id.name))
            cond = [('user_id', '=', user.id)]
            employee = self.env['hr.employee'].search(cond, limit=1)
            if not employee:
                raise UserError(
                    _('Employee not found for user: {}').format(
                        user.name))
        if vals.get('stage_id'):
            stage = self.env['event.track.stage'].browse(vals['stage_id'])
            if stage.is_done:
                for track in self:
                    track._create_analytic_line_with_displacement_product()
        return res

    def _create_analytic_line_with_displacement_product(self):
        analytic_line_obj = self.env['account.analytic.line']
        cond = [('partner_id', '=', self.partner_id.id)]
        user = self.env['res.users'].search(cond, limit=1)
        cond = [('user_id', '=', user.id)]
        employee = self.env['hr.employee'].search(cond, limit=1)
        if self.event_id.displacement_product_ids:
            for line in self.event_id.displacement_product_ids:
                cond = [('date', '=', self.date.date()),
                        ('partner_id', '=', self.partner_id.id),
                        ('event_track_id', '=', self.id),
                        ('product_id', '=', line.product_id.id)]
                if line.project_id:
                    cond.append(('project_id', '=', line.project_id.id))
                    if line.task_id:
                        cond.append(('task_id', '=', line.task_id.id))
                if not line.project_id and self.event_id.project_id:
                    cond.append(
                        ('project_id', '=', self.event_id.project_id.id))
                    if self.event_id.task_id:
                        cond.append(
                            ('task_id', '=', self.event_id.task_id.id))
                lines = analytic_line_obj.search(cond)
                if lines:
                    lines.unlink()
                vals = self._catch_values_for_create_analytic_line()
                name = vals.get('name')
                name = '{} {}'.format(name, line.product_id.name)
                vals.update({'name': name,
                             'unit_amount': 1,
                             'product_id': line.product_id.id,
                             'employee_id': employee.id})
                if line.project_id:
                    vals['project_id'] = line.project_id.id
                    if line.task_id:
                        vals['task_id'] = line.task_id.id
                if not line.project_id and self.event_id.project_id:
                    vals['project_id'] = self.event_id.project_id.id
                    if self.event_id.task_id:
                        vals['task_id'] = self.event_id.task_id.id
                analytic_line = self.create_analytic_line_from_track(
                    line, vals)
                analytic_line.amount = line.standard_price

    def create_analytic_line_from_track(self, line, vals):
        return self.env['account.analytic.line'].with_context(
            default_sale_order_id=line.sale_order_id,
            default_track_id=self).create(vals)
