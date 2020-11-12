# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    openupgrade.logged_query(
        cr, """
        UPDATE account_invoice inv SET (
            academic_year_id, school_id, course_id, child_id) = (
                SELECT
                    academic_year_id,
                    school_id,
                    course_id,
                    child_id
                FROM contract_contract c
                WHERE c.id IN (
                    SELECT cl.contract_id
                    FROM contract_line cl
                    WHERE cl.id IN (
                        SELECT il.contract_line_id
                        FROM account_invoice_line il
                        WHERE il.contract_line_id IS NOT NULL
                        AND il.invoice_id = inv.id)));
        """)
    openupgrade.logged_query(
        cr, """
        UPDATE account_move_line ml SET (
            academic_year_id, school_id, course_id, child_id) = (
                SELECT
                    academic_year_id,
                    school_id,
                    course_id,
                    child_id
                FROM account_invoice inv
                WHERE inv.id = ml.invoice_id);
        """)
