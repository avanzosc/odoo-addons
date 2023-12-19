# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    cr.execute("""
    UPDATE res_partner
       SET bus_passenger = 'yes'
     WHERE id IN (SELECT partner_id FROM fleet_route_stop_passenger)
        OR bus_passenger_tmp = True;
    """)
    cr.execute("""
    UPDATE res_partner
       SET bus_passenger = 'no'
     WHERE (bus_passenger != 'yes' or bus_passenger IS Null)
       AND educational_category IN ('student', 'otherchild');
    """)
