# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    openupgrade.logged_query(
        cr, """
        UPDATE account_invoice ref_inv SET (
            academic_year_id, school_id, course_id, child_id) = (
                SELECT
                    academic_year_id,
                    school_id,
                    course_id,
                    child_id
                FROM account_invoice inv
                WHERE inv.id = ref_inv.refund_invoice_id)
        WHERE
            type = 'out_refund'
            AND (academic_year_id IS NULL
                 OR school_id IS NULL
                 OR course_id IS NULL
                 OR child_id IS NULL);
        """)
