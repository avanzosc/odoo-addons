# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

fields_to_rename = [
    ('fleet.route.stop', 'fleet_route_stop', 'departure_estimated_time',
     'estimated_time'),
]


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    cr.execute(
        """
        SELECT *
        FROM fleet_route_stop
        WHERE direction = 'round';
        """)
    for stop in cr.dictfetchall():
        cr.execute(
            """
            INSERT INTO fleet_route_stop (
                name,
                departure_estimated_time,
                route_id,
                create_uid,
                create_date,
                write_uid,
                write_date,
                location_id,
                direction
            ) VALUES ('%s', %f, %d, %d, '%s', %d, '%s', %d, '%s')
            """ % (stop['name'], stop['return_estimated_time'],
                   stop['route_id'], stop['create_uid'], stop['create_date'],
                   stop['write_uid'], stop['write_date'],
                   stop['location_id'], 'coming'))
    cr.execute(
        """
        UPDATE fleet_route_stop
        SET direction = 'going'
        WHERE direction = 'round';
        """)
    cr.execute(
        """
        UPDATE fleet_route_stop
        SET departure_estimated_time = return_estimated_time
        WHERE direction = 'coming' AND return_estimated_time != 0.0;
        """)
    openupgrade.rename_fields(env, fields_to_rename)
