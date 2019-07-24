# Copyright 2019 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    category_restrict = fields.Many2one(comodel_name="category.restrict",
                                        string="Restricted To")


class CategoryRestrict(models.Model):
    _name = "category.restrict"
    _rec_name = "sequence"

    sequence = fields.Integer(string="Sequence")
    restricted_to = fields.Many2one(comodel_name="product.category",
                                    string="Restricted To")
    restricted_for = fields.Many2one(comodel_name="product.category",
                                     string="Restricted For")
