# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class CleaningDatabase(models.Model):
    _inherit = "cleaning.database"

    def action_delete_asset_operations(self):
        self.env.cr.execute(
            "DELETE FROM account_asset_line WHERE company_id in %s",
            [tuple(self.company_ids.ids)],
        )
        self.env.cr.execute(
            "DELETE FROM account_asset WHERE company_id in %s",
            [tuple(self.company_ids.ids)],
        )
