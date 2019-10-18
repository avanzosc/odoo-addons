# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    sale_line_id = fields.Many2one(
        comodel_name='sale.order.line',
        string='Sales Order Line',
        related='stock_move_id.sale_line_id',
        store=True)
    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sale Order',
        related='stock_move_id.sale_line_id.order_id',
        store=True)
    sale_user_id = fields.Many2one(
        comodel_name='res.users',
        string='Salesperson',
        related='stock_move_id.sale_line_id.order_id.user_id',
        store=True)
