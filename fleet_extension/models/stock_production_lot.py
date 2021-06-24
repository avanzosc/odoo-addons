# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    purchase_price = fields.Float(string='Purchase price')
    selling_price = fields.Float(string='Selling price')
    vehicle_id = fields.Many2one(
        string='Vehicle', comodel_name='fleet.vehicle')
    model_id = fields.Many2one(
        string='Model', comodel_name='fleet.vehicle.model',
        related='vehicle_id.model_id', store=True)
    license_plate = fields.Char(
        string='Actual license plate', related='vehicle_id.license_plate',
        store=True)
    license_plate_date = fields.Date(
        string='Actual license plate date',
        related='vehicle_id.license_plate_date', store=True)
    old_license_plate = fields.Char(
        string='First license plate',
        related='vehicle_id.old_license_plate', store=True)
    old_license_plate_date = fields.Date(
        string='First license plate date',
        related='vehicle_id.old_license_plate_date', store=True)
    type_id = fields.Many2one(
        string='Vehicle type', comodel_name='fleet.vehicle.model.type',
        related='model_id.type_id', store=True)

    @api.onchange("vehicle_id")
    def onchange_vehicle_id(self):
        if self.vehicle_id:
            if self.vehicle_id.product_id:
                self.product_id = self.vehicle_id.product_id
            else:
                self.vehicle_id.product_id = self.product_id

    @api.model
    def create(self, values):
        serial_number = super(StockProductionLot, self).create(values)
        if 'vehicle_id' in values and values.get('vehicle_id',
                                                 False):
            vehicle = self.env['fleet.vehicle'].browse(
                values.get('vehicle_id'))
            vehicle.serial_number_id = serial_number.id
        return serial_number

    def write(self, vals):
        if ('no_update_vehicle' not in self.env.context and
            'vehicle_id' in vals and vals.get('vehicle_id',
                                              False)):
            for serial_number in self:
                if (serial_number.vehicle_id and
                    serial_number.vehicle_id.id !=
                        vals.get('vehicle_id')):
                    serial_number.vehicle_id.serial_number_id = False
        result = super(StockProductionLot, self).write(vals)
        if ('no_update_vehicle' not in self.env.context and
            'vehicle_id' in vals and vals.get('vehicle_id',
                                              False)):
            vehicle = self.env['fleet.vehicle'].browse(
                vals.get('vehicle_id'))
            vehicle.with_context(
                no_update_serial_number=True).serial_number_id = self.id
        if ('no_update_product' not in self.env.context and
                'product_id' in vals and vals.get('product_id', False)):
            for lot in self.filtered(lambda x: x.product_id):
                lot.vehicle_id.with_context(
                    no_update_product=True).product_id = vals.get(
                        'product_id')
        return result
