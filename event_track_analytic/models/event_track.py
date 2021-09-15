# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, _
from odoo.exceptions import UserError


class EventTrack(models.Model):
    _inherit = 'event.track'

    project_id = fields.Many2one(
        string='Project', comodel_name='project.project', store=True,
        related='event_id.project_id')
    task_id = fields.Many2one(
        string='Task', comodel_name='project.task', store=True,
        related='event_id.task_id')
    analytic_account_id = fields.Many2one(
        string='Analytic account', comodel_name='account.analytic.account',
        related='event_id.analytic_account_id', store=True)
    account_analytic_line_ids = fields.One2many(
        string='Analytic lines', comodel_name='account.analytic.line',
        inverse_name='event_track_id')

    def _catch_values_for_create_analytic_line(self):
        name = u'{} {} {}'.format(
            self.event_id.name, self.name, self.date)
        analytic_line_vals = {
            'date': self.date,
            'unit_amount': self.duration,
            'name': name,
            'user_id': self.user_id.id,
            'event_id': self.event_id.id,
            'event_track_id': self.id}
        if self.analytic_account_id:
            analytic_line_vals['account_id'] = self.analytic_account_id.id
        if self.partner_id:
            cond = [('partner_id', '=', self.partner_id.id)]
            user = self.env['res.users'].search(cond, limit=1)
            if not user:
                raise UserError(
                    _('User not found for speaker: {}').format(
                        self.partner_id.name))
            cond = [('user_id', '=', user.id)]
            employee = self.env['hr.employee'].search(cond, limit=1)
            if not employee:
                raise UserError(
                    _('Employee not found for user: {}').format(
                        user.name))
            analytic_line_vals.update({
                'partner_id': self.partner_id.id,
                'employee_id': employee.id})
        return analytic_line_vals

    def _create_analytic_line(self):
        if self.event_id and not self.event_id.project_id:
            self.event_id.project_id = self.event_id._create_event_project().id
        values = self._catch_values_for_create_analytic_line()
        self.env['account.analytic.line'].create(values)

    def write(self, vals):
        res = super(EventTrack, self).write(vals)
        if vals.get('stage_id'):
            stage = self.env['event.track.stage'].browse(vals['stage_id'])
            if stage.is_done:
                for track in self:
                    cond = [('date', '=', track.date.date()),
                            ('partner_id', '=', track.partner_id.id),
                            ('event_track_id', '=', track.id)]
                    line = self.env['account.analytic.line'].search(
                        cond, limit=1)
                    if not line:
                        track._create_analytic_line()
        return res
