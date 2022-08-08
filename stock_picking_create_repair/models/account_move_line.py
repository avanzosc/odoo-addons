# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models, fields


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.model_create_multi
    def create(self, vals_list):
        result = super(AccountMoveLine, self).create(vals_list)
        for line in result:
            if line.sale_line_ids and len(line.sale_line_ids) == 1:
                sale_line = line.sale_line_ids[0]
                if (sale_line.is_repair and sale_line.product_to_repair_id):
                    line.write(
                        {"product_id": sale_line.product_to_repair_id.id,
                         "name": sale_line.product_to_repair_id.name})
        return result
