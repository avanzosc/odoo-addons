# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    root_category_id = fields.Many2one(
        comodel_name="product.category",
        string="Root Category",
        compute="_compute_root_category",
        store=True,
    )

    @api.depends("parent_id", "parent_path")
    def _compute_root_category(self):
        for categ in self:
            if categ.parent_id:
                root = categ.parent_path.split("/")
                root_category_id = self.env["product.category"].search(
                    [("id", "=", root[0])]
                )
                categ.root_category_id = root_category_id.id
            else:
                categ.root_category_id = categ.id
