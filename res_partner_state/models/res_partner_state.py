# -*- coding: utf-8 -*-
# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ResPartnerState(models.Model):
    _name = "res.partner.state"
    _description = "Customer state"
    _order = "name"

    name = fields.Char(
        string="Description", required=True, copy=False
    )
