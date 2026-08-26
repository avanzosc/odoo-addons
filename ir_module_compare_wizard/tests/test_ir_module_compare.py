# Copyright 2026 Ana Juaristi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from psycopg2 import IntegrityError

from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger


class TestIrModuleCompareWizard(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Wiz = cls.env["ir.module.import"]
        cls.Line = cls.env["ir.module.import.line"]
        cls.Module = cls.env["ir.module.module"]
        cls.Version = cls.env["odoo.version"]
        cls.wiz = cls.Wiz.create({"filename": "test.xls"})

    def _create_line(self, row):
        vals = self.wiz._get_line_values(row)
        vals["import_id"] = self.wiz.id
        return self.Line.create(vals)

    def _validate(self, line):
        line.write(line._action_validate())
        return line

    def _reset_base_module(self):
        base_mod = self.Module.search([("name", "=", "base")], limit=1)
        v17_18 = self.Version.search([("name", "in", ["17.0", "18.0"])])
        base_mod.sudo().write(
            {
                "included_in_core": True,
                "available_version_ids": [(6, 0, v17_18.ids)],
                "core_version_ids": [(6, 0, v17_18.ids)],
                "technical_description": "initial",
            }
        )
        return base_mod

    # ------------------------------------------------------------------
    # odoo.version
    # ------------------------------------------------------------------
    def test_seeded_versions_loaded(self):
        names = self.Version.search([]).mapped("name")
        for expected in ("8.0", "14.0", "16.0", "17.0", "18.0"):
            self.assertIn(expected, names)

    def test_unique_constraint_on_version_name(self):
        with self.assertRaises(IntegrityError), mute_logger("odoo.sql_db"):
            with self.cr.savepoint():
                self.Version.create({"name": "18.0"})

    # ------------------------------------------------------------------
    # _get_or_create_versions
    # ------------------------------------------------------------------
    def test_get_or_create_versions_mixed_separators_and_dedupe(self):
        before = self.Version.search_count([])
        versions = self.wiz._get_or_create_versions("19.5, 20.0; 18.0  19.5")
        self.assertEqual(sorted(versions.mapped("name")), ["18.0", "19.5", "20.0"])
        # 18.0 already existed; only 19.5 and 20.0 should have been created
        self.assertEqual(self.Version.search_count([]) - before, 2)

    def test_get_or_create_versions_empty_inputs(self):
        self.assertFalse(self.wiz._get_or_create_versions(""))
        self.assertFalse(self.wiz._get_or_create_versions(False))
        self.assertFalse(self.wiz._get_or_create_versions(None))

    # ------------------------------------------------------------------
    # included_in_core_provided flag
    # ------------------------------------------------------------------
    def test_provided_flag_false_when_column_absent(self):
        line = self._create_line(
            {"Technical Name": "base", "Available Versions": "18.0"}
        )
        self.assertFalse(line.included_in_core_provided)

    def test_provided_flag_true_when_column_present(self):
        line = self._create_line({"Technical Name": "base", "Included In Core": False})
        self.assertTrue(line.included_in_core_provided)

    def test_onchange_marks_provided_after_manual_edit(self):
        line = self._create_line(
            {"Technical Name": "base", "Available Versions": "18.0"}
        )
        self.assertFalse(line.included_in_core_provided)
        line.included_in_core = True
        line._onchange_included_in_core()
        self.assertTrue(line.included_in_core_provided)

    # ------------------------------------------------------------------
    # _action_validate write gating
    # ------------------------------------------------------------------
    def test_revalidate_with_no_migration_columns_preserves_module(self):
        base_mod = self._reset_base_module()
        line = self._create_line({"Technical Name": "base", "Notes": "x"})
        self._validate(line)
        self.assertTrue(base_mod.included_in_core)
        self.assertEqual(
            sorted(base_mod.available_version_ids.mapped("name")), ["17.0", "18.0"]
        )
        self.assertEqual(
            sorted(base_mod.core_version_ids.mapped("name")), ["17.0", "18.0"]
        )
        self.assertEqual(base_mod.technical_description, "initial")

    def test_partial_import_touches_only_provided_keys(self):
        base_mod = self._reset_base_module()
        line = self._create_line(
            {"Technical Name": "base", "Available Versions": "16.0, 17.0, 18.0"}
        )
        self._validate(line)
        # Available Versions overwritten, but everything else preserved
        self.assertTrue(base_mod.included_in_core)
        self.assertEqual(
            sorted(base_mod.available_version_ids.mapped("name")),
            ["16.0", "17.0", "18.0"],
        )
        self.assertEqual(
            sorted(base_mod.core_version_ids.mapped("name")), ["17.0", "18.0"]
        )
        self.assertEqual(base_mod.technical_description, "initial")

    def test_explicit_included_in_core_false_overrides_module(self):
        base_mod = self._reset_base_module()
        line = self._create_line({"Technical Name": "base", "Included In Core": False})
        self._validate(line)
        self.assertFalse(base_mod.included_in_core)

    def test_full_payload_writes_all_module_keys(self):
        base_mod = self._reset_base_module()
        line = self._create_line(
            {
                "Technical Name": "base",
                "Available Versions": "14.0, 15.0, 16.0",
                "Core Versions": "15.0, 16.0",
                "Included In Core": True,
                "Technical Description": "updated",
            }
        )
        self._validate(line)
        self.assertTrue(base_mod.included_in_core)
        self.assertEqual(
            sorted(base_mod.available_version_ids.mapped("name")),
            ["14.0", "15.0", "16.0"],
        )
        self.assertEqual(
            sorted(base_mod.core_version_ids.mapped("name")), ["15.0", "16.0"]
        )
        self.assertEqual(base_mod.technical_description, "updated")

    # ------------------------------------------------------------------
    # replaced_by lives on the line
    # ------------------------------------------------------------------
    def test_replaced_by_stays_on_line(self):
        line = self._create_line(
            {"Technical Name": "base", "Replaced By": "some_other_module"}
        )
        self.assertEqual(line.replaced_by, "some_other_module")
        self.assertNotIn("replaced_by", self.Module._fields)

    # ------------------------------------------------------------------
    # error state must not touch the module
    # ------------------------------------------------------------------
    def test_unknown_module_does_not_write(self):
        line = self._create_line(
            {
                "Technical Name": "this_module_does_not_exist_xyz",
                "Available Versions": "18.0",
                "Included In Core": True,
            }
        )
        self._validate(line)
        self.assertEqual(line.state, "error")
