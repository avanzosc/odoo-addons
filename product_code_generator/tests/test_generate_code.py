# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestGenerateCode(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.prefix = "07FA05001"
        cls.company = cls.env.company
        cls.company.barcode_prefix = 1234567
        cls.brand = cls.env["product.brand"].create({"name": "Test Brand", "code": "7"})
        cls.family = cls.env["product.category"].create(
            {"name": "Test Family", "code": "FA"}
        )
        cls.subfamily = cls.env["product.category"].create(
            {"name": "Test Subfamily", "parent_id": cls.family.id, "code": "05"}
        )
        cls.season = cls.env["seasonality"].create({"name": "Spring Test", "code": "1"})

    def _create_product(self, name, **extra):
        vals = {
            "name": name,
            "product_brand_id": self.brand.id,
            "family_id": self.family.id,
            "sub_family_id": self.subfamily.id,
            "season_id": self.season.id,
        }
        vals.update(extra)
        return self.env["product.product"].create(vals)

    def _expected_code(self, offset=0):
        code = self.env["product.code"].search([("name", "=", self.prefix)], limit=1)
        number = code.sequence_id.number_next_actual if code else 1
        return f"{self.prefix}{number + offset:03d}"

    def test_generate_code_creates_consecutive_references(self):
        first_expected = self._expected_code()
        second_expected = self._expected_code(offset=1)
        first = self._create_product("Product one")
        second = self._create_product("Product two")

        self.assertFalse(first.default_code)
        self.assertFalse(second.default_code)

        first.generate_code()
        second.generate_code()

        self.assertEqual(first.default_code, first_expected)
        self.assertEqual(second.default_code, second_expected)
        codes = self.env["product.code"].search([("name", "=", self.prefix)])
        self.assertEqual(len(codes), 1)

    def test_generate_code_keeps_existing_references(self):
        product = self._create_product("Manual reference", default_code="MANUAL-1")
        product.generate_code()
        self.assertEqual(product.default_code, "MANUAL-1")

    def test_generate_code_without_classification_uses_default_prefix(self):
        product = self.env["product.product"].create({"name": "No classification"})
        product.generate_code()
        self.assertTrue(product.default_code.startswith("000000000"))
        self.assertEqual(len(product.default_code), 12)

    def test_generate_code_from_template_updates_all_variants(self):
        attribute = self.env["product.attribute"].create({"name": "Test Colour"})
        red = self.env["product.attribute.value"].create(
            {"name": "Red", "attribute_id": attribute.id}
        )
        blue = self.env["product.attribute.value"].create(
            {"name": "Blue", "attribute_id": attribute.id}
        )
        template = self.env["product.template"].create(
            {
                "name": "Two colour template",
                "product_brand_id": self.brand.id,
                "family_id": self.family.id,
                "sub_family_id": self.subfamily.id,
                "season_id": self.season.id,
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": attribute.id,
                            "value_ids": [(6, 0, [red.id, blue.id])],
                        },
                    )
                ],
            }
        )
        variants = template.product_variant_ids
        self.assertEqual(len(variants), 2)
        expected = [self._expected_code(), self._expected_code(offset=1)]

        template.generate_code()

        self.assertEqual(sorted(variants.mapped("default_code")), sorted(expected))

    def test_generate_ean13_barcode(self):
        product = self._create_product("Barcode product")
        barcode = product._generate_ean13_barcode()
        self.assertEqual(len(barcode), 13)
        self.assertTrue(barcode.isdigit())
        self.assertEqual(barcode[:7], "1234567")
        self.assertEqual(
            barcode,
            self.env["product.product"]._ean13_with_checksum(barcode[:12]),
        )

    def test_generate_code_keeps_existing_barcode(self):
        product = self._create_product("Manual barcode", barcode="4006381333931")
        product.generate_code()
        self.assertEqual(product.barcode, "4006381333931")

    def test_barcode_sequence_is_created_and_reused(self):
        Product = self.env["product.product"]
        sequence = Product._get_barcode_sequence(self.company)
        self.assertEqual(sequence.code, "barcode.sequence")
        self.assertEqual(sequence.implementation, "no_gap")
        self.assertEqual(sequence.padding, 5)
        self.assertEqual(Product._get_barcode_sequence(self.company), sequence)

    def test_ean13_checksum_helper(self):
        Product = self.env["product.product"]
        check = Product._ean13_with_checksum("123456789012")
        self.assertEqual(len(check), 13)
        self.assertTrue(check.startswith("123456789012"))
        with self.assertRaises(UserError):
            Product._ean13_with_checksum("12345")

    def test_barcode_requires_company_prefix(self):
        self.company.barcode_prefix = 0
        product = self._create_product("No barcode prefix")
        with self.assertRaises(UserError):
            product._generate_ean13_barcode()
