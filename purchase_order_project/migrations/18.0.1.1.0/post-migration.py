from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    purchases = env["purchase.order"].search(
        [
            ("analytic_account_id", "!=", False),
            ("project_id", "=", False),
        ]
    )
    for purchase in purchases:
        projects = purchase.analytic_account_id.project_ids
        if len(projects) == 1:
            purchase.write(
                {
                    "project_id": projects[0].id,
                }
            )
