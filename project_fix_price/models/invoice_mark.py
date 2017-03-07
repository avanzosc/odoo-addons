# -*- coding: utf-8 -*-
# © 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models, fields


class InvoiceMark(models.Model):
    _name = 'invoice.mark'
    _rec_name = 'task_id'

    project_id = fields.Many2one(
        comodel_name='project.project', string='Project')
    task_id = fields.Many2one(comodel_name='project.task', string='Task')
    stage_id = fields.Many2one(
        comodel_name='project.task.type', string='Stage',
        related='task_id.stage_id')
    product_id = fields.Many2one(
        comodel_name='product.product', string='Product')
    date_end = fields.Date(
        related='task_id.date_deadline', string='Date end', store=True)
    percent = fields.Float(string='Percent')
    amount = fields.Float(string='Amount')
    invoice_id = fields.Many2one(
        comodel_name='account.invoice', related='task_id.invoice_id')

    @api.multi
    def create_invoice(self):
        for mark in self:
            mark.task_id.create_invoice()
