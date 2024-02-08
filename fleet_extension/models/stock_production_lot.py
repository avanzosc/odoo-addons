# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    purchase_price = fields.Float(string="Purchase price")
    selling_price = fields.Float(string="Selling price")
    model_id = fields.Many2one(
        string="Model",
        comodel_name="fleet.vehicle.model",
        related="vehicle_id.model_id",
        store=True,
    )
    license_plate = fields.Char(
        string="Actual license plate",
        related="vehicle_id.license_plate",
        store=True,
    )
    license_plate_date = fields.Date(
        string="Actual license plate date",
        related="vehicle_id.license_plate_date",
        store=True,
    )
    old_license_plate = fields.Char(
        string="First license plate",
        related="vehicle_id.old_license_plate",
        store=True,
    )
    old_license_plate_date = fields.Date(
        string="First license plate date",
        related="vehicle_id.old_license_plate_date",
        store=True,
    )
    type_id = fields.Many2one(
        string="Vehicle type",
        comodel_name="fleet.vehicle.model.type",
        related="model_id.type_id",
        store=True,
    )
    motor_guarantee = fields.Integer(
        string="Motor guarantee",
        related="product_id.motor_guarantee",
        store=True,
    )
    home_guarantee = fields.Integer(
        string="Home guarantee",
        related="product_id.home_guarantee",
        store=True,
    )
    watertightness_guarantee = fields.Integer(
        string="Watertightness guarantee",
        related="product_id.watertightness_guarantee",
        store=True,
    )
    motor_guarantee_unit = fields.Selection(
        string="Motor guarantee unit",
        default="year",
        related="product_id.motor_guarantee_unit",
        store=True,
    )
    home_guarantee_unit = fields.Selection(
        string="Home guarantee unit",
        default="year",
        related="product_id.home_guarantee_unit",
        store=True,
    )
    watertightness_guarantee_unit = fields.Selection(
        string="Watertightness guarantee unit",
        default="year",
        related="product_id.watertightness_guarantee_unit",
        store=True,
    )
    motor_guarantee_date = fields.Date(
        string="Motor guarantee date",
    )
    home_guarantee_date = fields.Date(
        string="Home guarantee date",
    )
    watertightness_guarantee_date = fields.Date(
        string="Watertightness guarantee date",
    )

    def _get_guarantee_dates(self, product_id=None):
        """Returns dates based on what's configured in current lot's product."""
        today = fields.Date.context_today(self)
        res = {}
        product = self.env["product.product"].browse(product_id) or self.product_id
        if product:
            if product.motor_guarantee:
                if product.motor_guarantee_unit == "year":
                    res["motor_guarantee_date"] = today + relativedelta(
                        years=product.motor_guarantee
                    )
                else:
                    res["motor_guarantee_date"] = today + relativedelta(
                        months=product.motor_guarantee
                    )
            if product.home_guarantee:
                if product.home_guarantee_unit == "year":
                    res["home_guarantee_date"] = today + relativedelta(
                        years=product.home_guarantee
                    )
                else:
                    res["home_guarantee_date"] = today + relativedelta(
                        months=product.home_guarantee
                    )
            if product.watertightness_guarantee:
                if product.watertightness_guarantee_unit == "year":
                    res["watertightness_guarantee_date"] = today + relativedelta(
                        years=product.watertightness_guarantee
                    )
                else:
                    res["watertightness_guarantee_date"] = today + relativedelta(
                        months=product.watertightness_guarantee
                    )
        return res

    # Assign dates according to products data
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            dates = self._get_guarantee_dates(
                vals.get("product_id") or self.env.context.get("default_product_id")
            )
            for d in dates:
                if not vals.get(d):
                    vals[d] = dates[d]
        return super().create(vals_list)
