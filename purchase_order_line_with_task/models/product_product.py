# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _convert_prepared_anglosaxon_line(self, line, partner):
        result = super(ProductProduct, self)._convert_prepared_anglosaxon_line(
            line, partner)
        # if 'allowed_task_ids' in line:
        #     result['allowed_task_ids'] = line.get('alloweb_task_ids')
        if "task_id" in line:
            result["task_id"] = line.get("task_id")
        return result
