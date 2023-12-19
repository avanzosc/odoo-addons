# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


def pre_init_hook(cr):
    put_project_in_analytic_line(cr)


def put_project_in_analytic_line(cr):
    cr.execute("""
        UPDATE account_analytic_line
        SET   project_id = (SELECT project_project.id
                            FROM   project_project,
                                   account_analytic_account
                            WHERE  account_analytic_account.id =
                                   account_analytic_line.account_id
                              AND  project_project.analytic_account_id =
                                   account_analytic_account.id
                              AND  1 = (SELECT COUNT(p.*)
                                        FROM project_project as p,
                                             account_analytic_account a
                                        WHERE a.id =
                                              account_analytic_line.account_id
                                          AND p.analytic_account_id = a.id))
        WHERE account_id is not null
          AND project_id is null
    """)
