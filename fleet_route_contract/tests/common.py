# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.contract_sale_school.tests.common import \
    ContractSaleSchoolCommon


class FleetRouteContractCommon(ContractSaleSchoolCommon):

    @classmethod
    def setUpClass(cls):
        super(FleetRouteContractCommon, cls).setUpClass()
        product_model = cls.env["product.product"]
        cls.route_model = cls.env["fleet.route"]
        cls.stop_model = cls.env["fleet.route.stop"]
        cls.passenger_model = cls.env["fleet.route.stop.passenger"]
        cls.complete_product = product_model.create({
            "name": "Complete Route",
            "recurrent_punctual": "recurrent",
            "month_start": cls.env.ref("base_month.base_month_november").id,
            "end_month": cls.env.ref("base_month.base_month_january").id,
        })
        cls.half_product = product_model.create({
            "name": "Half Route",
            "recurrent_punctual": "recurrent",
            "month_start": cls.env.ref("base_month.base_month_november").id,
            "end_month": cls.env.ref("base_month.base_month_january").id,
        })
        cls.route_name = cls.env["fleet.route.name"].create({
            "name": "Route",
            "complete_route_product_id": cls.complete_product.id,
            "half_route_product_id": cls.half_product.id,
        })
        cls.route_vals = {
            "name_id": cls.route_name.id,
            "direction": "going",
            "stop_ids": [(0, 0, {
                "name": "Stop",
            })],
        }
        cls.route_going = cls.route_model.create(cls.route_vals)
        cls.route_vals.update({
            "direction": "coming"
        })
        cls.route_coming = cls.route_model.create(cls.route_vals)
        cls.passenger = cls.passenger_model.create({
            "stop_id": cls.route_going.stop_ids[:1].id,
            "partner_id": cls.student.id,
        })
