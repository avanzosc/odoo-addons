# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from psycopg2.errors import UniqueViolation

from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestProductCodeSegments(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.code_model = cls.env["product.code"]
        cls.brand = cls.env["product.brand"].create({"name": "Test Brand", "code": "7"})
        cls.family = cls.env["product.category"].create(
            {"name": "Test Family", "code": "FA"}
        )
        cls.subfamily = cls.env["product.category"].create(
            {"name": "Test Subfamily", "parent_id": cls.family.id, "code": "05"}
        )
        cls.season = cls.env["seasonality"].create({"name": "Spring Test", "code": "1"})

    def test_brand_and_season_codes_are_zero_padded(self):
        self.assertEqual(self.brand.code, "07")
        self.assertEqual(self.season.code, "001")

        brand = self.env["product.brand"].create({"name": "Another Brand", "code": "3"})
        season = self.env["seasonality"].create({"name": "Autumn", "code": "12"})
        self.assertEqual(brand.code, "03")
        self.assertEqual(season.code, "012")

    def test_brand_default_code(self):
        brand = self.env["product.brand"].create({"name": "No Code Brand"})
        self.assertEqual(brand.code, "00")

    def test_writing_brand_and_season_codes_also_pads_them(self):
        self.brand.code = "4"
        self.season.code = "6"
        self.assertEqual(self.brand.code, "04")
        self.assertEqual(self.season.code, "006")

    def test_build_prefix_with_segments_and_without_them(self):
        prefix = self.code_model._build_prefix(
            self.brand, self.family, self.subfamily, self.season
        )
        self.assertEqual(prefix, "07FA05001")

        empty_prefix = self.code_model._build_prefix(
            self.env["product.brand"],
            self.env["product.category"],
            self.env["product.category"],
            self.env["seasonality"],
        )
        self.assertEqual(empty_prefix, "000000000")

    def test_code_create_builds_sequence_and_rejects_duplicates(self):
        vals = {
            "brand_id": self.brand.id,
            "family_id": self.family.id,
            "sub_family_id": self.subfamily.id,
            "season_id": self.season.id,
        }
        first = self.code_model.create(dict(vals))
        self.assertEqual(first.name, "07FA05001")
        self.assertEqual(first.sequence_id.name, "07FA05001")
        self.assertEqual(first.sequence_id.code, "product.product")
        self.assertEqual(first.sequence_id.implementation, "no_gap")
        self.assertEqual(first.sequence_id.padding, 3)
        self.assertFalse(first.sequence_id.use_date_range)

        with self.assertRaises(UniqueViolation), self.env.cr.savepoint():
            self.code_model.create(dict(vals))

    def test_code_create_computes_name_even_when_supplied(self):
        sequence = self.env["ir.sequence"].create(
            {"name": "Custom sequence", "code": "product.product", "padding": 4}
        )
        code = self.code_model.create(
            {"name": "CUSTOM", "sequence_id": sequence.id, "brand_id": self.brand.id}
        )
        self.assertEqual(code.name, "070000000")
        self.assertEqual(code.sequence_id, sequence)

    def test_name_is_recomputed_when_segment_codes_change(self):
        code = self.code_model.create(
            {
                "brand_id": self.brand.id,
                "family_id": self.family.id,
                "sub_family_id": self.subfamily.id,
                "season_id": self.season.id,
            }
        )
        self.season.code = "2"
        self.assertEqual(code.name, "07FA05002")

    def test_duplicate_prefix_from_other_segments_is_rejected(self):
        self.code_model.create(
            {
                "brand_id": self.brand.id,
                "family_id": self.family.id,
                "sub_family_id": self.subfamily.id,
                "season_id": self.season.id,
            }
        )
        brand = self.env["product.brand"].create({"name": "Other brand", "code": "07"})
        family = self.env["product.category"].create(
            {"name": "Other family", "code": "FA"}
        )
        subfamily = self.env["product.category"].create(
            {"name": "Other subfamily", "code": "05"}
        )
        season = self.env["seasonality"].create({"name": "Other season", "code": "001"})
        with self.assertRaises(UniqueViolation), self.env.cr.savepoint():
            self.code_model.create(
                {
                    "brand_id": brand.id,
                    "family_id": family.id,
                    "sub_family_id": subfamily.id,
                    "season_id": season.id,
                }
            )

    def test_sequence_number_next_inverse_updates_sequence(self):
        code = self.code_model.create(
            {
                "brand_id": self.brand.id,
                "family_id": self.family.id,
                "sub_family_id": self.subfamily.id,
                "season_id": self.season.id,
            }
        )
        code.sequence_number_next = 25
        self.assertEqual(code.sequence_id.number_next_actual, 25)
        self.assertEqual(code.sequence_number_next, 25)

    def test_onchange_family_sets_category(self):
        template = self.env["product.template"].new(
            {"family_id": self.family.id, "sub_family_id": self.subfamily.id}
        )
        template._onchange_family()
        self.assertEqual(template.categ_id, self.subfamily)

        template.sub_family_id = False
        template._onchange_family()
        self.assertEqual(template.categ_id, self.family)

    def test_access_rights(self):
        user = self.env["res.users"].create(
            {
                "name": "PCG read only user",
                "login": "pcg_read_only_user",
                "groups_id": [(6, 0, [self.env.ref("base.group_user").id])],
            }
        )
        user_env = self.env(user=user)
        self.assertTrue(
            user_env["product.code"].check_access_rights("read", raise_exception=False)
        )
        self.assertFalse(
            user_env["product.code"].check_access_rights(
                "create", raise_exception=False
            )
        )

    def test_company_barcode_prefix_validation(self):
        with self.assertRaises(ValidationError):
            self.env.company.barcode_prefix = 10000000
