# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class CancellationReason(models.Model):
    _name = 'cancellation.reason'
    _description = 'Cancellation Reason'

    name = fields.Char(string='Name')
