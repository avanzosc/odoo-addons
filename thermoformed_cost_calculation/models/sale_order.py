# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    thermoformed_id = fields.Many2one(
        string='Thermoformed', comodel_name='thermoformed.cost')
