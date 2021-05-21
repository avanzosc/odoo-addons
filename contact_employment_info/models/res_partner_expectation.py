# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ResPartnerExpectation(models.Model):
    _name = 'res.partner.expectation'
    _description = 'Expectation'

    name = fields.Char(string='Expectation', required=True)
