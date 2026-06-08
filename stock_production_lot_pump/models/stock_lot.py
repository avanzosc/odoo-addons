# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockLot(models.Model):
    _inherit = "stock.lot"

    customer_tag_number = fields.Char(copy=False)
    plant_location = fields.Char(copy=False)
    vehicular_fluid = fields.Char(copy=False)
    caudal = fields.Integer(string="Caudal (m3/h)", default=0, copy=False)
    pressure = fields.Integer(string="Pressure (Bar)", default=0, copy=False)
    temperature = fields.Integer(default=0, copy=False)
    impeller_trim = fields.Integer(default=0, copy=False)
    engine_power = fields.Integer(default=0, copy=False)
    engine_speed = fields.Integer(default=0, copy=False)
    atex_zone = fields.Boolean(default=False, copy=False)
    application_description = fields.Text(copy=False)
    high_date = fields.Date(copy=False)
    low_date = fields.Date(copy=False)
    maintenance_status = fields.Text(copy=False)
    modifications_made_to_the_pump = fields.Text(copy=False)
    notes = fields.Text(copy=False)
