# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from .common import FleetRouteContractCommon
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestFleetRouteContract(FleetRouteContractCommon):

    def test_add_passenger_half_product(self):
        contract = self.get_contract()
        self.assertTrue(contract)
        self.assertIn(
            self.half_product, contract.mapped("contract_line_ids.product_id"))

    def test_add_passenger_complete_product(self):
        self.passenger_model.create({
            "stop_id": self.route_coming.stop_ids[:1].id,
            "partner_id": self.student.id,
        })
        contract = self.get_contract()
        self.assertTrue(contract)
        self.assertIn(
            self.complete_product, contract.mapped(
                "contract_line_ids.product_id"))

    def test_add_passenger_passenger_product(self):
        self.passenger.write({
            "route_product_id": self.complete_product.id,
        })
        contract = self.get_contract()
        self.assertTrue(contract)
        self.assertIn(
            self.complete_product, contract.mapped(
                "contract_line_ids.product_id"))

    def get_contract(self):
        contract_domain = [
            ("child_id", "=", self.student.id),
            ("academic_year_id", "=", self.academic_year.id),
        ]
        self.assertFalse(self.contract_model.search(contract_domain))
        self.student.add_passenger_contract_line()
        return self.contract_model.search(contract_domain)
