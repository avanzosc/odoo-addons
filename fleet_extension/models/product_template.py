# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    motor_guarantee = fields.Integer(string="Motor guarantee")
    home_guarantee = fields.Integer(string="Home guarantee")
    watertightness_guarantee = fields.Integer(string="Watertightness guarantee")
    motor_guarantee_unit = fields.Selection(
        [("month", "Month"), ("year", "Year")],
        string="Motor guarantee unit",
        default="year",
    )
    home_guarantee_unit = fields.Selection(
        [("month", "Month"), ("year", "Year")],
        string="Home guarantee unit",
        default="year",
    )
    watertightness_guarantee_unit = fields.Selection(
        [("month", "Month"), ("year", "Year")],
        string="Watertightness guarantee unit",
        default="year",
    )
    collection_id = fields.Many2one(
        string="Collection", comodel_name="fleet.vehicle.model.collection"
    )
    mam = fields.Integer(string="Maximum authorized mass")
    motor_model_id = fields.Many2one(
        string="Motor model", comodel_name="fleet.vehicle.model"
    )
    displacement = fields.Char(string="Displacement")
    horsepower = fields.Integer(string="Horsepower")
    seats = fields.Integer(string="Seats Number")
    doors = fields.Integer(string="Doors Number", default=5)
    sleeping_places = fields.Integer(string="Number of sleeping places")
    fuel_type = fields.Selection(
        [
            ("gasoline", "Gasoline"),
            ("diesel", "Diesel"),
            ("lpg", "LPG"),
            ("electric", "Electric"),
            ("hybrid", "Hybrid"),
        ],
        string="Fuel Type",
    )
    country_id = fields.Many2one(string="Country", comodel_name="res.country")
    chassis_model_id = fields.Many2one(
        string="Chassis Model", comodel_name="fleet.vehicle.model"
    )
