# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    cr.execute("""
        UPDATE res_partner
        SET educational_category = 'otherchild'
        WHERE educational_category = 'other';
    """)
    cr.execute("""
        UPDATE res_partner
        SET educational_category = 'other'
        WHERE educational_category IS NULL;
    """)
