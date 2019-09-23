# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

models_to_rename = [
    # Fleet Route Stop
    ('fleet.itinerary', 'fleet.route.stop'),
]
tables_to_rename = [
    #  Fleet Route Stop
    ('fleet_itinerary', 'fleet_route_stop'),
]
columns_to_copy = {
    'fleet_route_stop': [
        ('stop_id', 'location_id', None),
    ],
}


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    openupgrade.rename_models(cr, models_to_rename)
    openupgrade.rename_tables(cr, tables_to_rename)
    openupgrade.copy_columns(cr, columns_to_copy)
