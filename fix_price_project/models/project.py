# -*- coding: utf-8 -*-
# © 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import _, api, exceptions, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    mark_ids = fields.One2many(
        comodel_name='invoice.mark', string='Marks', inverse_name='project_id')


class ProjectTask(models.Model):
    _inherit = 'project.task'

    is_mark = fields.Boolean(
        default=False, compute='_compute_is_mark', store=True)
    invoiced = fields.Boolean(default=False)
    mark_ids = fields.One2many(
        comodel_name='invoice.mark', string='Marks', inverse_name='task_id')

    @api.multi
    def _prepare_invoice_vals(self, mark):
        invoice_line_vals = {
            'product_id': mark.product_id.id,
            'name': mark.product_id.name,
            'price_unit': mark.amount,
            'quantity': 1.0,
        }
        return invoice_line_vals

    @api.multi
    def create_invoice(self):
        invoice_line = []
        inv_obj = self.env['account.invoice']
        for task in self:
            partner_id = task.project_id.partner_id
            if not partner_id:
                raise exceptions.Warning(
                    _('The project hasn\'t customer. If you want to invoice '
                      'this task, please select one.'))
            if not task.ended:
                raise exceptions.Warning(
                    _('This task should be ended before making the invoice.'))
            for line in task.mark_ids:
                invoice_line.append(self._prepare_invoice_vals(line))
            if not invoice_line:
                raise exceptions.Warning(
                    _('Nothing to invoice. Please create an invoice '
                      'mark for this task: %s') % (task.name))
            inv_values = {
                'partner_id': partner_id.id,
                'type': 'out_invoice',
                'origin': task.name,
                'account_id': partner_id.property_account_receivable.id,
                'invoice_line': [(0, 0, inv_line) for inv_line in invoice_line]
            }
            inv_id = inv_obj.create(inv_values)
            task.invoiced = True
            return {
                'name': _('Customer Invoices'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'account.invoice',
                'view_id': self.env.ref('account.invoice_form').id,
                'type': 'ir.actions.act_window',
                'target': 'current',
                'res_id': inv_id.id or False
            }

    @api.multi
    @api.depends('mark_ids')
    def _compute_is_mark(self):
        for record in self:
            record.is_mark = True if record.mark_ids else False
