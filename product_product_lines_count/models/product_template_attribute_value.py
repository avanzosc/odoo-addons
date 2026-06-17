# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class ProductTemplateAttributeValue(models.Model):
    _inherit = "product.template.attribute.value"
    
    def _ids2str(self):
        return ','.join([str(i) for i in sorted(self.ids)])
