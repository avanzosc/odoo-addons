# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api, _


class EventEvent(models.Model):
    _inherit = 'event.event'

    project_id = fields.Many2one(
        string='Project', comodel_name='project.project', copy=False)
    task_id = fields.Many2one(
        string='Task', comodel_name='project.task', copy=False)
    analytic_account_id = fields.Many2one(
        string='Analytic account', comodel_name='account.analytic.account',
        related='project_id.analytic_account_id', store=True)
    account_analytic_line_ids = fields.One2many(
        string='Analytic lines', comodel_name='account.analytic.line',
        inverse_name='event_id')
    count_sale_orders = fields.Integer(
        string='# Sale orders', compute='_compute_count_sale_orders')
    count_sale_orders_lines = fields.Integer(
        string='# Sale orders lines', compute='_compute_count_sale_orders')

    def _compute_count_sale_orders(self):
        for event in self:
            event.count_sale_orders_lines = len(event.sale_order_lines_ids)
            sales = event.sale_order_lines_ids.mapped('order_id')
            event.count_sale_orders = len(sales)

    def write(self, vals):
        confirmed_stage = self.env.ref('event.event_stage_announced')
        result = super(EventEvent, self).write(vals)
        if ('stage_id' in vals and
                vals.get('stage_id', False) == confirmed_stage.id):
            for event in self.filtered(lambda x: not x.project_id):
                event.search_project_in_sale_line()
        return result

    def search_project_in_sale_line(self):
        for ticket in self.event_ticket_ids:
            project = self.env['project.project']
            task = self.env['project.task']
            cond = [('event_id', '=', ticket.event_id.id),
                    ('event_ticket_id', '=', ticket.id)]
            sale_line = self.env['sale.order.line'].search(cond)
            if not sale_line:
                project = self._create_event_project()
                task = self._create_event_task(project, ticket)
            if sale_line and len(sale_line) == 1:
                if not sale_line.project_id:
                    sale_line._timesheet_create_project()
                project = sale_line.project_id
                if (not sale_line.task_id and sale_line.is_service and
                    sale_line.product_id.sale_ok and
                    sale_line.product_id.service_tracking in (
                        'task_global_project', 'task_in_project')):
                    sale_line._timesheet_create_task(project=project)
                if sale_line.task_id:
                    task = sale_line.task_id
            if project and not self.project_id:
                self.project_id = project.id
            if task:
                ticket.task_id = task.id
        if not self.task_id:
            tasks = self.env['project.task']
            lines = self.event_ticket_ids.filtered(lambda x: x.task_id)
            for line in lines:
                if line.task_id not in tasks:
                    tasks += line.task_id
            if len(tasks) == 1:
                self.task_id = tasks.id

    def _create_event_project(self):
        project_vals = self.values_for_create_project()
        return self.env['project.project'].create(project_vals)

    def values_for_create_project(self):
        project_vals = {
            'name': self.name,
            'bill_type': 'customer_project',
            'allow_billable': True}
        if self.customer_id:
            project_vals['partner_id'] = self.customer_id.id
            if self.customer_id.email:
                project_vals['partner_email'] = self.customer_id.email
            if self.customer_id.phone:
                project_vals['partner_phone'] = self.customer_id.phone
        return project_vals

    def _create_event_task(self, project, ticket):
        task_vals = self.values_for_create_task(project, ticket)
        return self.env['project.task'].create(task_vals)

    def values_for_create_task(self, project, ticket):
        task_vals = {
            'project_id': project.id,
            'name': ticket.name,
            'description': ticket.name,
            'company_id': project.company_id.id}
        if self.customer_id:
            task_vals['partner_id'] = self.customer_id.id
            if self.customer_id.email:
                task_vals['partner_email'] = self.customer_id.email
            if self.customer_id.phone:
                task_vals['partner_phone'] = self.customer_id.phone
        return task_vals

    @api.onchange("project_id")
    def _onchange_project_id(self):
        if 'no_update_project' not in self.env.context and self.project_id:
            self.with_context(
                no_update_name=True).name = self.project_id.name

    @api.onchange("name")
    def _onchange_name(self):
        if ('no_update_name' not in self.env.context and self.name and
                self.project_id):
            self.project_id.with_context(
                no_update_project=True).name = self.name

    def button_show_sale_order_from_event(self):
        if self.sale_order_lines_ids:
            sales = self.sale_order_lines_ids.mapped('order_id')
            context = self.env.context.copy()
            return {
                'name': _('Sale orders'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': context,
                'domain': [('id', 'in', sales.ids)]}

    def button_show_sale_order_line_from_event(self):
        if self.sale_order_lines_ids:
            context = self.env.context.copy()
            context.update(
                {'default_event_id': self.id})
            return {
                'name': _('Sale orders lines'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order.line',
                'context': context,
                'domain': [('id', 'in', self.sale_order_lines_ids.ids)]}
