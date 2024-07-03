# Copyright 2024 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade  # pylint: disable=W7936

fields_to_rename = [
    ("product.packaging.import.line", "product_packaging_import_line", "length",
     "packaging_length"),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_fields(env, fields_to_rename)
