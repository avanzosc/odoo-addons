# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class CancelReason(models.Model):
    _name = 'cancel.reason'
    _description = 'Cancel Reason'

    name = fields.Char(string='Name')
