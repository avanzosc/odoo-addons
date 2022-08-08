# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_repair = fields.Boolean(
        string="Is repair", default=False, copy=False)

    @api.onchange('type')
    def _onchange_type(self):
        result = super(ProductTemplate, self)._onchange_type()
        for template in self:
            if template.type != "service":
                template.is_repair = False
        return result
