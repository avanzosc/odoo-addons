# -*- coding: utf-8 -*-
# © 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import _, api, exceptions, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    mark_ids = fields.One2many(
        comodel_name='invoice.mark', string='Marks', inverse_name='project_id')

    @api.multi
    @api.constrains('mark_ids')
    def _check_mark_amount_and_percent(self):
        for project in self.filtered(lambda x: x.fix_price_invoices):
            all_percent = sum(project.mark_ids.mapped('percent'))
            all_amount = sum(project.mark_ids.mapped('amount'))
            if all_percent > 100:
                raise exceptions.Warning(
                    _('The sum of percent cant be greather than 100!'))
            if all_amount > project.analytic_account_id.amount_max:
                raise exceptions.Warning(
                    _('The sum of amount cant be greather than %s!') %
                    (project.amount_max))


class ProjectTask(models.Model):
    _inherit = 'project.task'

    is_mark = fields.Boolean(
        default=False, compute='_compute_is_mark', store=True)
    invoice_id = fields.Many2one(
        comodel_name='account.invoice', string='Invoice')
    mark_ids = fields.One2many(
        comodel_name='invoice.mark', string='Marks', inverse_name='task_id')

    @api.multi
    def _prepare_invoice_vals(self, mark):
        account = mark.product_id.property_account_income or \
            mark.product_id.categ_id.property_account_income_categ
        analytic = mark.project_id.analytic_account_id
        if not account:
                raise exceptions.Warning(
                    _("Please define income account for product '%s'.") %
                    mark.product_id.name)
        taxes = mark.product_id.taxes_id or account.tax_ids
        tax = analytic.partner_id.property_account_position.map_tax(taxes)
        invoice_line_vals = {
            'product_id': mark.product_id.id,
            'name': u"{}-{}".format(mark.project_id.name, mark.task_id.name),
            'price_unit': mark.amount,
            'account_id': account.id,
            'quantity': 1.0,
            'account_analytic_id': analytic.id,
            'invoice_line_tax_id': [(6, 0, tax.ids)],
        }
        return invoice_line_vals

    @api.multi
    def create_invoice(self):
        invoice_line = []
        inv_obj = self.env['account.invoice']
        type_obj = self.env['project.task.type']
        end_type = type_obj.search([('ending', '=', True)], limit=1)
        for task in self:
            partner_id = task.project_id.partner_id
            if not task.ended:
                task.stage_id = end_type
            if not partner_id:
                raise exceptions.Warning(
                    _('The project hasn\'t customer. If you want to invoice '
                      'this task, please select one.'))
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
            inv_id.button_reset_taxes()
            task.write({'invoice_id': inv_id.id})
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

    @api.multi
    def write(self, values):
        res = super(ProjectTask, self).write(values)
        if values.get('stage_id'):
            for task in self.filtered(lambda x: x.ended and not x.invoice_id):
                task.create_invoice()
        return res
