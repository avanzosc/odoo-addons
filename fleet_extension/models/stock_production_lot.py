# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api
from datetime import date
from dateutil import relativedelta


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
    motor_guarantee = fields.Integer(
        string='Motor guarantee', related='product_id.motor_guarantee',
        store=True)
    home_guarantee = fields.Integer(
        string='Home guarantee', related='product_id.home_guarantee',
        store=True)
    watertightness_guarantee = fields.Integer(
        string='Watertightness guarantee',
        related='product_id.watertightness_guarantee', store=True)
    motor_guarantee_unit = fields.Selection(
        string="Motor guarantee unit", default="year",
        related='product_id.motor_guarantee_unit', store=True)
    home_guarantee_unit = fields.Selection(
        string="Home guarantee unit", default="year",
        related='product_id.home_guarantee_unit', store=True)
    watertightness_guarantee_unit = fields.Selection(
        string="Watertightness guarantee unit", default="year",
        related='product_id.watertightness_guarantee_unit', store=True)
    motor_guarantee_date = fields.Date(
        string='Motor guarantee date', compute='_compute_guarantee_dates',
        store=True)
    home_guarantee_date = fields.Date(
        string='Home guarantee date', compute='_compute_guarantee_dates',
        store=True)
    watertightness_guarantee_date = fields.Date(
        string='Watertightness guarantee date',
        compute='_compute_guarantee_dates', store=True)

    @api.onchange("vehicle_id")
    def onchange_vehicle_id(self):
        if self.vehicle_id:
            if self.vehicle_id.product_id:
                self.product_id = self.vehicle_id.product_id.id
            else:
                self.vehicle_id.product_id = self.product_id.id

    @api.depends("motor_guarantee", "home_guarantee",
                  "watertightness_guarantee",
                  "motor_guarantee_unit",
                  "home_guarantee_unit",
                  "watertightness_guarantee_unit")
    def _compute_guarantee_dates(self):
        for lot in self:
            if lot.motor_guarantee:
                today = date.today()
                if lot.motor_guarantee_unit == 'year':
                    lot.motor_guarantee_date = (
                        today + relativedelta.relativedelta(
                            years=lot.motor_guarantee))
                else:
                    lot.motor_guarantee_date = (
                        today + relativedelta.relativedelta(
                            months=lot.motor_guarantee))
            if lot.home_guarantee:
                if lot.home_guarantee_unit == 'year':
                    lot.home_guarantee_date = (
                        today + relativedelta.relativedelta(
                            years=lot.home_guarantee))
                else:
                    lot.home_guarantee_date = (
                        today + relativedelta.relativedelta(
                            months=lot.home_guarantee))
            if lot.watertightness_guarantee:
                if lot.watertightness_guarantee_unit == 'year':
                    lot.watertightness_guarantee_date = (
                        today + relativedelta.relativedelta(
                            years=lot.watertightness_guarantee))
                else:
                    lot.watertightness_guarantee_date = (
                        today + relativedelta.relativedelta(
                            months=lot.watertightness_guarantee))

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
