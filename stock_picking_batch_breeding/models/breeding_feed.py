# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class BreedingFeed(models.Model):
    _name = "breeding.feed"
    _description = "Breeding Feed"

    name = fields.Char(string='Name')
