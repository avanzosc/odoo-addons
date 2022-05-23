# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    campaign_id = fields.Many2one(
        string='Campaign', comodel_name='utm.campaign',
        related='task_id.sale_order_id.campaign_id', store=True)
    medium_id = fields.Many2one(
        string='Medium', comodel_name='utm.medium',
        related='task_id.sale_order_id.medium_id', store=True)
    source_id = fields.Many2one(
        string='Source', comodel_name='utm.source',
        related='task_id.sale_order_id.source_id', store=True)
