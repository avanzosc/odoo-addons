# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, api


class StockLocation(models.Model):
    _inherit = 'stock.location'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        result = super(StockLocation, self).name_search(
            name=name, args=args, operator=operator, limit=limit)
        if not name:
            return result
        my_name = '%{}%'.format(name)
        cond = [('warehouse_id', 'ilike', my_name)]
        warehouses = self.search(cond)
        for warehouse in warehouses:
            found = False
            for line in result:
                if line and line[0] == warehouse.id:
                    found = True
                    break
            if not found:
                result.append((warehouse.id, warehouse.name))
        return result
