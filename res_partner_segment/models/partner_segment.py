# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class PartnerSegment(models.Model):
    _name = "partner.segment"
    _description = "Partner Segment"

    name = fields.Char(required=True)
