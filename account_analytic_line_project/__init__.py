from . import models
from odoo import api, SUPERUSER_ID


def _post_install_put_project_in_analytic_lines(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        account_analytic_line_obj = env["account.analytic.line"]
        lines = account_analytic_line_obj.search(
            [("project_id", "=", False), ("account_id", "!=", False)]
        )
        for line in lines:
            if line.account_id.project_ids:
                line.project_id = line.account_id.project_ids[0].id
