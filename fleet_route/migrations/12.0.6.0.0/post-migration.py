# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    for route in env["fleet.route"].search([]):
        new_route = route.copy(
            default={"direction": "coming"})

        cr.execute("""
        SELECT manager_id_tmp, manager_phone_mobile_tmp
          FROM fleet_route
         WHERE id = %d
        """ % (route.id))
        for values in cr.dictfetchall():
            if values["manager_id_tmp"]:
                cr.execute("""
                UPDATE fleet_route
                   SET manager_id = %d,
                       manager_phone_mobile = %s
                 WHERE route_id = %d
                """ % (values["manager_id_tmp"],
                       values["manager_phone_mobile_tmp"],
                       new_route.id))
        cr.execute("""
        SELECT id
          FROM fleet_route_stop
         WHERE direction_tmp = 'coming'
           AND route_id = %d
        """ % (route.id))
        for stop in cr.dictfetchall():
            cr.execute("""
            UPDATE fleet_route_stop
               SET route_id = %d
             WHERE id = %d
            """ % (new_route.id, stop["id"]))
    cr.execute("""
    ALTER TABLE fleet_route
    DROP COLUMN manager_id_tmp
    """)
    cr.execute("""
    ALTER TABLE fleet_route
    DROP COLUMN manager_phone_mobile_tmp
    """)
    cr.execute("""
    ALTER TABLE fleet_route_stop
    DROP COLUMN direction_tmp
    """)
