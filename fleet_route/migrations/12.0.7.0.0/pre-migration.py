# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    cr.execute(
        """
        CREATE TABLE IF NOT EXISTS fleet_route_name (
            id SERIAL NOT NULL,
            name VARCHAR UNIQUE NOT NULL,
            PRIMARY KEY(id)
        );
        """)
    cr.execute(
        """
        INSERT INTO fleet_route_name (name)
        SELECT DISTINCT name FROM fleet_route;
        """)
    cr.execute(
        """
        ALTER TABLE fleet_route
        ADD name_id INTEGER;
        """)
    cr.execute(
        """
        UPDATE fleet_route AS r
        SET name_id = (SELECT id
                       FROM fleet_route_name AS n
                       WHERE n.name = r.name);
        """)
