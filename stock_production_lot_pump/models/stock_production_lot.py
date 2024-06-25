# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    customer_tag_number = fields.Char(string="Customer tag number", copy=False)
    plant_location = fields.Char(string="Plant location", copy=False)
    vehicular_fluid = fields.Char(string="Vehicular fluid", copy=False)
    caudal = fields.Integer(string="Caudal (m3/h)", default=0, copy=False)
    pressure = fields.Integer(string="Pressure (Bar)", default=0, copy=False)
    temperature = fields.Integer(string="Temperature", default=0, copy=False)
    impeller_trim = fields.Integer(string="Impeller trim", default=0, copy=False)
    engine_power = fields.Integer(string="Engine power", default=0, copy=False)
    engine_speed = fields.Integer(string="Engine speed", default=0, copy=False)
    atex_zone = fields.Boolean(string="Atex zone", default=False, copy=False)
    application_description = fields.Text(string="Application description", copy=False)
    high_date = fields.Date(string="High date", copy=False)
    low_date = fields.Date(string="Low date", copy=False)
    maintenance_status = fields.Text(string="Maintenance status", copy=False)
    modifications_made_to_the_pump = fields.Text(
        string="Modifications made to the pump", copy=False
    )
    notes = fields.Text(string="Notes", copy=False)
