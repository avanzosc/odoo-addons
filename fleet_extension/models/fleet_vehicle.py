# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    license_plate = fields.Char(string='Actual license plate', copy=False)
    license_plate_date = fields.Date(
        string='Actual license plate date', copy=False)
    old_license_plate = fields.Char(string='First license plate', copy=False)
    old_license_plate_date = fields.Date(
        string='First license plate date', copy=False)
    tag_ids = fields.Many2many(string='Distribution')
    motor_model_id = fields.Many2one(
        string='Motor model', comodel_name='fleet.vehicle.model')
    displacement = fields.Integer(string='Displacement')
    sleeping_places = fields.Integer(string='Number of sleeping places')
    key_amount = fields.Integer(string='Keys amount')
    upholstery = fields.Char(string='Upholstery')
    furniture = fields.Char(string='Furniture')
    mam = fields.Integer(string='Maximum authorized mass')
    product_id = fields.Many2one(
        string='Product', comodel_name='product.product')
    purchase_price = fields.Float(string='Purchase price')
    retail_price = fields.Float(string='Retail price')
    promotion_price = fields.Float(string='Promotion price')
    promotion_name = fields.Char(string='Promotion name')
    type_id = fields.Many2one(
        string='Vehicle type', comodel_name='fleet.vehicle.model.type',
        related='model_id.type_id', store=True)
    serial_number_id = fields.Many2one(
        string='Serial number', comodel_name='stock.production.lot',
        copy=False)

    @api.onchange("serial_number_id")
    def onchange_serial_number_id(self):
        if self.serial_number_id:
            if self.serial_number_id.product_id:
                self.product_id = self.serial_number_id.product_id

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        result = super(FleetVehicle, self).name_search(
            name=name, args=args, operator=operator, limit=limit)
        if not name:
            return result
        my_name = '%{}%'.format(name)
        cond = ['|', ('license_plate', 'ilike', my_name),
                ('old_license_plate', 'ilike', my_name)]
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
    def search_read(
            self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain2 = False
        domain3 = False
        for d in domain:
            if d and d[0] == 'name':
                domain2 = [['license_plate', d[1], d[2]]]
                domain3 = [['old_license_plate', d[1], d[2]]]
        result = super(FleetVehicle, self).search_read(
            domain=domain, fields=fields, offset=offset, limit=limit,
            order=order)
        if domain2:
            result2 = super(FleetVehicle, self).search_read(
                domain=domain2, fields=fields, offset=offset, limit=limit,
                order=order)
            if result2:
                found = False
                for line in result2:
                    if line in result:
                        found = True
                if not found:
                    result += result2
        if domain3:
            result3 = super(FleetVehicle, self).search_read(
                domain=domain3, fields=fields, offset=offset, limit=limit,
                order=order)
            if result3:
                found = False
                for line in result3:
                    if line in result:
                        found = True
                if not found:
                    result += result3
        return result

    @api.model
    def create(self, values):
        vehicle = super(FleetVehicle, self).create(values)
        if 'serial_number_id' in values and values.get('serial_number_id',
                                                       False):
            serial_number = self.env['stock.production.lot'].browse(
                values.get('serial_number_id'))
            serial_number.with_context(
                no_update_vehicle=True).vehicle_id = vehicle.id
        return vehicle

    def write(self, vals):
        if (('no_update_serial_number' not in self.env.context) and (
            'serial_number_id' in vals) and (
                vals.get('serial_number_id', False))):
            for vehicle in self:
                if (vehicle.serial_number_id and
                    vehicle.serial_number_id.id != vals.get(
                        'serial_number_id')):
                    vehicle.serial_number_id.vehicle_id = False
        result = super(FleetVehicle, self).write(vals)
        if ('no_update_serial_number' not in self.env.context and (
            'serial_number_id' in vals and vals.get(
                'serial_number_id', False))):
            serial_number = self.env['stock.production.lot'].browse(
                vals.get('serial_number_id'))
            serial_number.with_context(
                no_update_vehicle=True).vehicle_id = self.id
        if ('no_update_product' not in self.env.context and
                'product_id' in vals and vals.get('product_id', False)):
            for vehicle in self.filtered(lambda x: x.product_id):
                vehicle.serial_number_id.with_context(
                    no_update_product=True).product_id = vals.get(
                        'product_id')
        return result
