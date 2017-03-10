# -*- coding: utf-8 -*-
# © 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.multi
    @api.depends('line_ids', 'line_ids.invoice_id', 'line_ids.unit_amount')
    def _compute_consumed_hours(self):
        for record in self:
            not_invoiced = record.line_ids.filtered(lambda x: not x.invoice_id)
            record.consumed_hours = sum(not_invoiced.mapped('unit_amount'))

    @api.multi
    @api.depends('hours_per_month', 'consumed_hours')
    def _compute_remaining_hours_calc(self):
        for record in self:
            record.remaining_hours_month = (
                record.hours_per_month and (record.hours_per_month -
                                            record.consumed_hours) or 0.0)

    hours_per_month = fields.Float(string='Hours per month')
    consumed_hours = fields.Float(
        compute='_compute_consumed_hours', string="Consumed Hours", store=True)
    remaining_hours_month = fields.Float(
        compute='_compute_remaining_hours_calc',
        string='Remaining Time', store=True)


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    @api.model
    def _prepare_cost_invoice_line(
            self, invoice_id, product_id, uom, user_id, factor_id, account,
            analytic_lines, journal_type, data):
        res = super(AccountAnalyticLine, self)._prepare_cost_invoice_line(
            invoice_id=invoice_id, product_id=product_id, uom=uom,
            user_id=user_id, factor_id=factor_id, account=account,
            analytic_lines=analytic_lines, journal_type=journal_type,
            data=data)
        total_qty = sum(l.qty_invoice for l in analytic_lines)
        res.update({
            'quantity': total_qty,
        })
        return res

    @api.multi
    @api.depends('unit_amount', 'account_id', 'account_id.hours_per_month',
                 'invoice_id')
    def _compute_qty_invoice(self):
        unit_amount = 0
        invoiced = 0
        for record in self.filtered(lambda x: not x.invoice_id):
            hours_per_month = record.account_id.hours_per_month
            unit_amount += record.unit_amount
            if unit_amount > hours_per_month:
                record.qty_invoice = \
                    unit_amount - (hours_per_month + invoiced)
                invoiced += record.qty_invoice

    qty_invoice = fields.Float(
        string='Qty to invoice', compute='_compute_qty_invoice')
