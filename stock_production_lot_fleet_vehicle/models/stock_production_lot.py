# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    vehicle_id = fields.Many2one(
        string='Vehicle', comodel_name='fleet.vehicle')

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
        return result
