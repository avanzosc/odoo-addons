# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def write(self, values):
        result = super(SaleOrderLine, self).write(values)
        if "name" in values:
            for line in self:
                if line.move_ids:
                    line.move_ids.write({"name": line.name})
        return result
