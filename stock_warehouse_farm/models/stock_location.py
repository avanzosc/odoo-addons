# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockLocation(models.Model):
    _inherit = 'stock.location'

    type_id = fields.Many2one(
        string='Section',
        comodel_name='category.type')
    activity = fields.Selection(
        [('fattening', 'Fattening'),
         ('incubation', 'Incubation'),
         ('reproduction', 'Reproduction'),
         ('recry', 'Recry'),
         ('birth', 'Birth')], string="Activity", copy=False,
        related="warehouse_id.activity",
        store=True)
    is_hatchery = fields.Boolean(string="Is Hatchery", default=False)

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        result = super(StockLocation, self).name_search(
            name=name, args=args, operator=operator, limit=limit)
        if not name:
            return result
        my_name = '%{}%'.format(name)
        cond = [('warehouse_id', 'ilike', my_name), ("usage", "=", "internal")]
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
