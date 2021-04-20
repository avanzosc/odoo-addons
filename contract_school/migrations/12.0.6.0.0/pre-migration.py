# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    openupgrade.logged_query(
        cr, """
        ALTER TABLE account_payment_line
        ADD COLUMN academic_year_id integer,
        ADD COLUMN center_id integer,
        ADD COLUMN course_id integer,
        ADD COLUMN student_id integer;
        """)
    openupgrade.logged_query(
        cr, """
        ALTER TABLE bank_payment_line
        ADD COLUMN academic_year_id integer,
        ADD COLUMN center_id integer,
        ADD COLUMN course_id integer,
        ADD COLUMN student_id integer;
        """)
    openupgrade.logged_query(
        cr, """
        UPDATE account_payment_line pay_line SET (
            academic_year_id, center_id, course_id, student_id) = (
                SELECT
                    academic_year_id,
                    school_id,
                    course_id,
                    child_id
                FROM account_move_line move_line
                WHERE move_line.id = pay_line.move_line_id)
        WHERE
            academic_year_id IS NULL
            OR center_id IS NULL
            OR course_id IS NULL
            OR student_id IS NULL;
        """)
    openupgrade.logged_query(
        cr, """
        UPDATE bank_payment_line bank_line SET (
            academic_year_id, center_id, course_id, student_id) = (
                SELECT
                    academic_year_id,
                    center_id,
                    course_id,
                    student_id
                FROM account_payment_line pay_line
                WHERE bank_line.id = pay_line.bank_line_id
                LIMIT 1)
        WHERE
            academic_year_id IS NULL
            OR center_id IS NULL
            OR course_id IS NULL
            OR student_id IS NULL;
        """)
    openupgrade.logged_query(
        cr, """
        UPDATE account_move_line move_line SET (
            academic_year_id, school_id, course_id, child_id) = (
                SELECT
                    academic_year_id,
                    center_id,
                    course_id,
                    student_id
                FROM bank_payment_line bank_line
                WHERE move_line.bank_payment_line_id = bank_line.id)
        WHERE
            bank_payment_line_id IS NOT NULL AND
            (academic_year_id IS NULL
             OR school_id IS NULL
             OR course_id IS NULL
             OR child_id IS NULL);
        """)
