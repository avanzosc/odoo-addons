# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api, _


class RepairOrder(models.Model):
    _inherit = 'repair.order'

    employee_id = fields.Many2one(
        string='Employee', comodel_name='hr.employee')
    expected_repair_date = fields.Date(
        string='Expected repair date')
    fees_lines = fields.One2many(readonly=False)
    operations = fields.One2many(readonly=False)
    only_read = fields.Boolean(
        string='Only read', compute='_compute_only_read')
    show_button_repair_start_intecpla = fields.Boolean(
        string='Show button repair start intecpla',
        compute='_compute_show_button_repair_start_intecpla')
    task_state = fields.Selection(
        selection=[('uninitiated', _('Task Uninitiated')),
                   ('in_progress', _(' Task In progress')),
                   ('finished', _(' Task Finished'))],
        string='Task state', compute='_compute_task_state', store=True)

    def _compute_only_read(self):
        for repair in self:
            if (repair.state in ('confirmed', 'done', '2binvoiced') or
                repair.invoiced or
                    (repair.state == 'under_repair' and repair.finished_task)):
                repair.only_read = True
            else:
                repair.only_read = False

    def _compute_show_button_repair_start_intecpla(self):
        for repair in self:
            show = False
            if repair.state == 'under_repair' and repair.finished_task:
                show = True
            repair.show_button_repair_start_intecpla = show

    @api.depends('state', 'finished_task')
    def _compute_task_state(self):
        for repair in self:
            task_state = 'uninitiated'
            if repair.state == 'under_repair' and not repair.finished_task:
                task_state = 'in_progress'
            if repair.state == 'done' or repair.repaired or repair.finished_task:
                task_state = 'finished'
            repair.task_state = task_state

    @api.multi
    def action_invoice_create(self, group=False):
        result = super(RepairOrder, self.with_context(
            no_catch_notes=True)).action_invoice_create(group=group)
        return result

    def action_repair_start_intecpla(self):
        self.write({'finished_task': False})

    @api.multi
    def action_cancel_validation(self):
        found = False
        if (len(self) == 1 and self.state == '2binvoiced' and
                self.invoice_method == 'b4repair'):
            found = True
        result = super(RepairOrder, self).action_cancel_validation()
        for repair in self:
            if found:
                repair.write({'state': 'draft'})
            else:
                repair.write({'state': 'confirmed'})
        return result
