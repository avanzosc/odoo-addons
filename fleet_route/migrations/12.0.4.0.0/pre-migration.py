# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

fields_to_rename = [
    ('fleet.route', 'fleet_route', 'manager_id', 'going_manager_id'),
    ('fleet.route', 'fleet_route', 'manager_phone_mobile',
     'going_manager_phone_mobile'),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_fields(env, fields_to_rename)
