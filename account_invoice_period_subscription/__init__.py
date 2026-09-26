from . import models


def _post_install_put_dates_in_invoice(env):
    move_lines = env["account.move.line"].search(
        [
            ("deferred_start_date", "!=", False),
            ("deferred_end_date", "!=", False),
        ]
    )
    invoices = move_lines.mapped("move_id")
    invoices.put_subscription_dates()
