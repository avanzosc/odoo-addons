# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    cr.execute("""
        UPDATE calendar_event e
           SET academic_year_id = (
                SELECT school_year_id
                  FROM hr_employee_supervised_year t
                 WHERE t.id = e.supervised_year_id)
         WHERE supervised_year_id IS NOT Null AND academic_year_id IS Null;
    """)
