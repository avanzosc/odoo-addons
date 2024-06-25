# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    labeled_length = fields.Char(string="Length", copy=False)
    description_label_es = fields.Char(string="Description label (es)", copy=False)
    description_label_fr = fields.Char(string="Description label (fr)", copy=False)
    description_label_en = fields.Char(string="Description label (en)", copy=False)
    labeled_finished_code = fields.Char(string="Finished code", copy=False)
    labeled_color_es = fields.Char(string="Color (es)", copy=False)
    labeled_color_fr = fields.Char(string="Color (fr)", copy=False)
    labeled_color_en = fields.Char(string="Color (en)", copy=False)
