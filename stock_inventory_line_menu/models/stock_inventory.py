# -*- coding: utf-8 -*-
# Copyright 2019 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    inventory_lines_count = fields.Integer(
        string="Lines count", compute="_compute_inventory_lines_count")

    @api.multi
    def _compute_inventory_lines_count(self):
        lines_obj = self.env['stock.inventory.line']
        for inventory in self:
            inventory.inventory_lines_count = lines_obj.search_count([
                ('inventory_id', '=', inventory.id)])

    @api.multi
    def action_open_inventory_lines(self):
        template_obj = self.env['product.template']
        result = template_obj._get_act_window_dict(
            'stock_inventory_line_menu.action_inventory_line')
        result['domain'] = "[('inventory_id', '=', %d)]" % self.id
        result['context'] = {'search_default_internal_loc': 1}
        return result


class StockInventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    date = fields.Datetime(string="Date", related="inventory_id.date",
                           store=True)
