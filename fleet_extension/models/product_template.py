# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api
from datetime import date
from dateutil import relativedelta


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    motor_guarantee = fields.Integer(string='Motor guarantee')
    home_guarantee = fields.Integer(string='Home guarantee')
    watertightness_guarantee = fields.Integer(
        string='Watertightness guarantee')
    motor_guarantee_unit = fields.Selection(
        [("month", "Month"), ("year", "Year")], string="Motor guarantee unit",
        default="year")
    home_guarantee_unit = fields.Selection(
        [("month", "Month"), ("year", "Year")], string="Home guarantee unit",
        default="year")
    watertightness_guarantee_unit = fields.Selection(
        [("month", "Month"), ("year", "Year")],
        string="Watertightness guarantee unit", default="year")
    motor_guarantee_date = fields.Date(
        string='Motor guarantee date')
    home_guarantee_date = fields.Date(
        string='Home guarantee date')
    watertightness_guarantee_date = fields.Date(
        string='Watertightness guarantee date')

    @api.onchange("motor_guarantee", "home_guarantee",
                  "watertightness_guarantee", "motor_guarantee_unit",
                  "home_guarantee_unit", "watertightness_guarantee_unit")
    def onchange_guarantee_dates(self):
        if self.motor_guarantee:
            today = date.today()
            if self.motor_guarantee_unit == 'year':
                self.motor_guarantee_date = (
                    today + relativedelta.relativedelta(
                        years=self.motor_guarantee))
            else:
                self.motor_guarantee_date = (
                    today + relativedelta.relativedelta(
                        months=self.motor_guarantee))
        if self.home_guarantee:
            if self.home_guarantee_unit == 'year':
                self.home_guarantee_date = (
                    today + relativedelta.relativedelta(
                        years=self.home_guarantee))
            else:
                self.home_guarantee_date = (
                    today + relativedelta.relativedelta(
                        months=self.home_guarantee))
        if self.watertightness_guarantee:
            if self.watertightness_guarantee_unit == 'year':
                self.watertightness_guarantee_date = (
                    today + relativedelta.relativedelta(
                        years=self.watertightness_guarantee))
            else:
                self.watertightness_guarantee_date = (
                    today + relativedelta.relativedelta(
                        months=self.watertightness_guarantee))
