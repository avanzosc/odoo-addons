# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    substitutions = env["hr.employee.supervised.year.substitution"].search([])
    for substitution in substitutions:
        events = substitution._search_calendars()
        cr.execute(
            """
            UPDATE calendar_event e
               SET substitute_teacher_id = %s
             WHERE e.id IN %s
            """, (substitution.substitute_teacher_id.id, tuple(events.ids)))
