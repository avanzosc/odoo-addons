# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    margin_purchase = fields.Float(
        string='Default Purchase Margin', default=10.0)
    value_added_margin = fields.Float(
        string='Default Value Added Margin', default=20.0)
    costs_operator = fields.Float(
        string='Costs Operator')
    costs_mechanic = fields.Float(
        string='Costs Mechanic')
