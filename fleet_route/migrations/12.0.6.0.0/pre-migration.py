# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

fields_to_rename = [
    ("fleet.route", "fleet_route", "going_manager_id", "manager_id"),
    ("fleet.route", "fleet_route", "going_manager_phone_mobile",
     "manager_phone_mobile"),
    ("fleet.route", "fleet_route", "coming_manager_id", "manager_id_tmp"),
    ("fleet.route", "fleet_route", "coming_manager_phone_mobile",
     "manager_phone_mobile_tmp"),
    ("fleet.route.stop", "fleet_route_stop", "direction", "direction_tmp"),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_fields(env, fields_to_rename)
