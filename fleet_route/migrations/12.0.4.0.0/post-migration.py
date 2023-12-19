# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    cr.execute(
        """
        UPDATE fleet_route_stop
           SET direction = 'coming'
         WHERE departure_estimated_time = 0
           AND return_estimated_time != 0
        """)
    cr.execute(
        """
        UPDATE fleet_route_stop
           SET direction = 'going'
         WHERE departure_estimated_time != 0
           AND return_estimated_time = 0
        """)
