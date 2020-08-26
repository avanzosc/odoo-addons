# Copyright 2018 Maite Esnal - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    kind_id = fields.Many2one(
        comodel_name='account.analytic.line.kind', string='Kind')


class AccountAnalyticLineKind(models.Model):
    _name = 'account.analytic.line.kind'
    _description = 'Analytic Line Kind'

    name = fields.Char(string='Name', required=True, translate=True)
