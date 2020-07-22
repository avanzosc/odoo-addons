# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class FleetRouteName(models.Model):
    _name = "fleet.route.name"
    _description = "Route Name"
    _order = "name"

    name = fields.Char(string="Name")
    route_ids = fields.One2many(
        comodel_name="fleet.route", inverse_name="name_id",
        string="Routes")
    complete_route_product_id = fields.Many2one(
        comodel_name="product.product", string="Complete route product")
    complete_route_product_price = fields.Float(
        string="Complete route product price",
        related="complete_route_product_id.lst_price")
    half_route_product_id = fields.Many2one(
        comodel_name="product.product", string="Half route product")
    half_route_product_price = fields.Float(
        string="Half route product price",
        related="half_route_product_id.lst_price")
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Route name must be unique!')
    ]
