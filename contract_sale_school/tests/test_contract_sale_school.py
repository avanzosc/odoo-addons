# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from .common import ContractSaleSchoolCommon
from odoo.tests import common
from odoo.exceptions import ValidationError


@common.at_install(False)
@common.post_install(True)
class TestContractSaleSchool(ContractSaleSchoolCommon):

    def test_contract_sale_school_exception(self):
        self.sale_order.academic_year_id = False
        self.service.recurrent_punctual = 'punctual'
        with self.assertRaises(ValidationError):
            self.sale_order.action_confirm()

    def test_contract_sale_school_multiple_payer(self):
        sale_line_vals = {
            "product_id": self.recurrent_product.id,
            "name": self.recurrent_product.name,
            "product_uom": self.recurrent_product.uom_id.id,
            "price_unit": self.recurrent_product.list_price,
        }
        self.sale_order.order_line = [(0, 0, sale_line_vals)]
        with self.assertRaises(ValidationError):
            self.sale_order.action_confirm()
        order_line = self.sale_order.order_line.filtered(
            lambda l: l.product_id == self.recurrent_product)
        order_line.write({
            "payer_ids": [
                (0, 0, {
                    "payer_id": self.progenitor.id,
                    "pay_percentage": 25.0,
                    "bank_id": self.progenitor.bank_ids[:1].id,
                }),
                (0, 0, {
                    "payer_id": self.relative.id,
                    "pay_percentage": 75.0,
                    "bank_id": self.relative.bank_ids[:1].id,
                })],
        })
        self.sale_order.action_confirm()
        self.assertEqual(self.sale_order.contracts_count, 2)
        action_dict = self.sale_order.action_view_contracts()
        self.assertIn(
            ("sale_id", "in", self.sale_order.ids), action_dict.get("domain"))
        contract = self.sale_order.contract_ids.filtered(
            lambda c: c.partner_id == self.progenitor)
        self.assertEqual(len(contract.contract_line_ids), 1)
        line = contract.contract_line_ids[:1]
        self.assertEqual(line.payment_percentage, 25.0)

    def test_contract_sale_school_recurrent(self):
        sale_line_vals = {
            "product_id": self.recurrent_product.id,
            "name": self.recurrent_product.name,
            "product_uom": self.recurrent_product.uom_id.id,
            "price_unit": self.recurrent_product.list_price,
            "payer_ids": [
                (0, 0, {
                    "payer_id": self.progenitor.id,
                    "pay_percentage": 100,
                    "bank_id": self.progenitor.bank_ids[:1].id,
                })],
        }
        self.sale_order.order_line = [(0, 0, sale_line_vals)]
        self.sale_order.action_confirm()
        self.assertEqual(self.sale_order.contracts_count, 1)
        contract = self.sale_order.contract_ids.filtered(
            lambda c: c.partner_id == self.progenitor)
        self.assertEqual(len(contract.contract_line_ids), 1)
        for line in contract.contract_line_ids:
            self.assertEqual(line.payment_percentage, 100.0)

    def test_contract_sale_school_punctual(self):
        sale_line_vals = {
            "product_id": self.product_punctual.id,
            "name": self.product_punctual.name,
            "product_uom": self.product_punctual.uom_id.id,
            "price_unit": self.product_punctual.list_price,
            "payer_ids": [
                (0, 0, {
                    "payer_id": self.progenitor.id,
                    "pay_percentage": 100.0,
                    "bank_id": self.progenitor.bank_ids[:1].id,
                })],
        }
        self.sale_order.order_line = [(0, 0, sale_line_vals)]
        self.sale_order.action_confirm()
        self.assertEqual(self.sale_order.contracts_count, 1)
        contract = self.sale_order.contract_ids.filtered(
            lambda c: c.partner_id == self.progenitor)
        self.assertEqual(len(contract.contract_line_ids), 2)
        for line in contract.contract_line_ids:
            self.assertEqual(line.payment_percentage, 100.0)

    def test_contract_sale_school_multiple_banks(self):
        self.progenitor.write({
            "bank_ids": [(0, 0, {
                "acc_number": "ES6601542128217651556524",
            })],
        })
        sale_line_vals = [{
            "product_id": self.product_punctual.id,
            "name": self.product_punctual.name,
            "product_uom": self.product_punctual.uom_id.id,
            "price_unit": self.product_punctual.list_price,
            "payer_ids": [
                (0, 0, {
                    "payer_id": self.progenitor.id,
                    "pay_percentage": 100.0,
                    "bank_id": self.progenitor.bank_ids[:1].id,
                })],
        }, {
            "product_id": self.product_punctual.id,
            "name": self.product_punctual.name,
            "product_uom": self.product_punctual.uom_id.id,
            "price_unit": self.product_punctual.list_price,
            "payer_ids": [
                (0, 0, {
                    "payer_id": self.progenitor.id,
                    "pay_percentage": 100.0,
                    "bank_id": self.progenitor.bank_ids[1:].id,
                })],
        }]
        self.sale_order.order_line = [(0, 0, x) for x in sale_line_vals]
        self.sale_order.action_confirm()
        self.assertEqual(self.sale_order.contracts_count, 2)
