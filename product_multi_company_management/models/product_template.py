# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.onchange("company_ids")
    def _onchange_company_ids(self):
        self.ensure_one()
        if len(self.company_ids) == 1:
            self.company_id = self.company_ids[:1].id
        else:
            self.company_id = False
