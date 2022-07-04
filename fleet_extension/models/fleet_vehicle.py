# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    license_plate = fields.Char(string="Actual license plate", copy=False)
    license_plate_date = fields.Date(string="Actual license plate date", copy=False)
    old_license_plate = fields.Char(string="First license plate", copy=False)
    old_license_plate_date = fields.Date(string="First license plate date", copy=False)
    tag_ids = fields.Many2many(string="Distribution")
    motor_model_id = fields.Many2one(
        string="Motor model",
        comodel_name="fleet.vehicle.model",
    )
    displacement = fields.Char(
        string="Displacement",
    )
    sleeping_places = fields.Integer(string="Number of sleeping places")
    key_number = fields.Char(string="Key Number")
    house_number = fields.Char(string="House Number")
    upholstery = fields.Char(string="Upholstery")
    furniture = fields.Char(string="Furniture")
    mam = fields.Integer(
        string="Maximum authorized mass", related="product_id.mam", store=True
    )
    purchase_price = fields.Float(string="Purchase price")
    retail_price = fields.Float(string="Retail price")
    promotion_price = fields.Float(string="Promotion price")
    promotion_name = fields.Char(string="Promotion name")
    motor_guarantee_date = fields.Date(
        string="Motor guarantee date",
        related="serial_number_id.motor_guarantee_date",
        store=True,
    )
    home_guarantee_date = fields.Date(
        string="Home guarantee date",
        related="serial_number_id.home_guarantee_date",
        store=True,
    )
    watertightness_guarantee_date = fields.Date(
        string="Watertightness guarantee date",
        related="serial_number_id.watertightness_guarantee_date",
        store=True,
    )
    collection_id = fields.Many2one(
        string="Collection", comodel_name="fleet.vehicle.model.collection"
    )
    range_id = fields.Many2one(
        string="Range",
        comodel_name="fleet.vehicle.range",
        related="model_id.range_id",
        store=True,
    )
    chassis_model_id = fields.Many2one(
        string="Chassis Model",
        comodel_name="fleet.vehicle.model",
    )

    @api.onchange("product_id")
    def onchange_product_id(self):
        if self.product_id:
            self.seats = self.product_id.seats
            self.doors = self.product_id.doors
            self.sleeping_places = self.product_id.sleeping_places
            self.fuel_type = self.product_id.fuel_type
            self.motor_model_id = self.product_id.motor_model_id
            self.chassis_model_id = self.product_id.chassis_model_id
            self.displacement = self.product_id.displacement
            self.horsepower = self.product_id.horsepower

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        result = super(FleetVehicle, self).name_search(
            name=name, args=args, operator=operator, limit=limit
        )
        if not name:
            return result
        my_name = "%{}%".format(name)
        cond = [
            "|",
            ("license_plate", "ilike", my_name),
            ("old_license_plate", "ilike", my_name),
        ]
        vehicles = self.search(cond)
        for vehicle in vehicles:
            found = False
            for line in result:
                if line and line[0] == vehicle.id:
                    found = True
                    break
            if not found:
                result.append((vehicle.id, vehicle.name))
        return result

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain2 = False
        for d in domain:
            if d and d[0] == "name":
                domain2 = [["old_license_plate", d[1], d[2]]]
        result = super(FleetVehicle, self).search_read(
            domain=domain, fields=fields, offset=offset, limit=limit, order=order
        )
        if domain2:
            result2 = super(FleetVehicle, self).search_read(
                domain=domain2, fields=fields, offset=offset, limit=limit, order=order
            )
            if result2:
                found = False
                for line in result2:
                    if line in result:
                        found = True
                if not found:
                    result += result2
        return result
