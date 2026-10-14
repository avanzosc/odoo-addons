# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class QcTest(models.Model):
    _inherit = "qc.test"

    name = fields.Char(copy=False)

    _sql_constraints = [
        (
            "qc_test_name_unique",
            "UNIQUE(name)",
            "Already exists a quality test with this name.",
        ),
    ]

    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})

        if not default.get("name"):
            base_name = self.name
            new_name = f"{base_name} (copy)"
            counter = 2

            while self.search_count([("name", "=", new_name)]):
                new_name = f"{base_name} (copy {counter})"
                counter += 1

            default["name"] = new_name

        return super().copy(default)
