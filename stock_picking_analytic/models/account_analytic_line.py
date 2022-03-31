# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    stock_move_id = fields.Many2one(
        comodel_name='stock.move', string='Stock Move')
    picking_id = fields.Many2one(
        comodel_name='stock.picking', string='Picking',
        related='stock_move_id.picking_id', store=True)
