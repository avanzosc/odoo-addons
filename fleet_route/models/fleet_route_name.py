# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class FleetRouteName(models.Model):
    _name = "fleet.route.name"
    _description = "Route Name"

    name = fields.Char(string="Name")
    route_ids = fields.One2many(
        comodel_name="fleet.route", inverse_name="name_id",
        string="Routes")

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Route name must be unique!')
    ]
