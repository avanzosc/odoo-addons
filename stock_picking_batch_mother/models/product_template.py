# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    requires_mother = fields.Boolean(
        string='Requires Mother',
        default=False)
    is_hen = fields.Boolean(
        string="Hen",
        default=False)

