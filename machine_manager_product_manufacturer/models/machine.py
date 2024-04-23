# -*- coding: utf-8 -*-
# Copyright 2015 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class Machine(models.Model):
    _inherit = "machine"

    manufacturer_id = fields.Many2one(
        string="Manufacturer", comodel_name="res.partner",
        related="product_id.manufacturer_id", readonly=True, store=True,
        help="Manufacturer is related to the associated product defined for "
        "the machine."
    )
