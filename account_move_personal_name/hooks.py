from odoo import SUPERUSER_ID, api

BATCH_SIZE = 500


def post_init_hook(env):
    env = api.Environment(env.cr, SUPERUSER_ID, {})

    companies = env["res.company"].search([])
    companies._create_personal_name_sequence()

    while True:
        moves = env["account.move"].search(
            [
                ("state", "=", "posted"),
                ("personal_name", "=", False),
            ],
            order="company_id, date, id",
            limit=BATCH_SIZE,
        )

        if not moves:
            break

        values = []

        for move in moves:
            seq = (
                env["ir.sequence"]
                .with_company(move.company_id)
                .next_by_code(
                    "account.move.personal.name",
                    sequence_date=move.date,
                )
            )

            values.append((f"{move.date.year}{seq}", move.id))

        env.cr.executemany(
            """
            UPDATE account_move
               SET personal_name = %s
             WHERE id = %s
            """,
            values,
        )

        env.cr.commit()
        env.invalidate_all()
