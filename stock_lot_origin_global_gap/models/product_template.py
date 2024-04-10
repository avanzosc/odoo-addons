# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    show_origin_global_gap_in_documents = fields.Boolean(
        string="Show Origin/Glogal Gap in documents", default=True, copy=False
    )
