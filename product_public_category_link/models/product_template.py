# Copyright 2025 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.onchange("categ_id")
    def _onchange_categ_id_sync_public_categories(self):
        if self.categ_id and self.categ_id.public_category:
            self.public_categ_ids |= self.categ_id.public_category
