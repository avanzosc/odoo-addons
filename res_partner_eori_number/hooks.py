# Copyright 2024 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

fields_to_rename = [
    (
        "res.partner",
        "res_partner",
        "x_studio_eori_number",
        "eori_code",
    ),
]


def remove_studio(env):
    cr = env.cr
    if openupgrade.column_exists(cr, "res_partner", "x_studio_eori_number"):
        openupgrade.rename_fields(env, fields_to_rename)
