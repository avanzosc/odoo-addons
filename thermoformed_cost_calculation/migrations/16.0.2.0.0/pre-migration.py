# Copyright 2025 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

_column_renames = {
    "thermoformed_cost": [
        ("costs_kilo", "material_cost"),
        ("costs_hour", "workcenter_cost"),
        ("costs_operator", "operator_cost"),
        ("costs_mechanic", "mechanic_cost"),
        ("costs_box", "box_cost"),
        ("costs_pallet", "pallet_cost"),
        ("costs_pallet_transport", "pallet_transport_cost"),
    ],
}


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_columns(env.cr, _column_renames)
