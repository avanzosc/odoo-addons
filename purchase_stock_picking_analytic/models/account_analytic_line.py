# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    purchase_line_id = fields.Many2one(
        comodel_name='purchase.order.line',
        string='Purchase Order Line',
        related='stock_move_id.purchase_line_id',
        store=True)
    purchase_order_id = fields.Many2one(
        comodel_name='purchase.order',
        string='Purchase Order',
        related='stock_move_id.purchase_line_id.order_id',
        store=True)
    purchase_user_id = fields.Many2one(
        comodel_name='res.users',
        string='Purchase Representative',
        related='stock_move_id.purchase_line_id.order_id.user_id',
        store=True)
