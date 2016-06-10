# -*- coding: utf-8 -*-
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models, _


class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    @api.model
    def _get_available_filters(self):
        """This function will return the list of filters allowed according to
        the options checked in 'Settings/Warehouse'.

        :return: list of tuple
        """
        res_filters = super(StockInventory, self)._get_available_filters()
        res_filters.append(('ondate', _('Inventory on a date')))
        return res_filters

    filter = fields.Selection(
        selection=_get_available_filters, string='Selection Filter',
        required=True)
    date = fields.Datetime(readonly=False, states={})
    location_childs = fields.Boolean(
        readonly=True, states={'draft': [('readonly', False)]},
        help='With this check it will search also in the child locations of'
        ' the selected location.', string='Get location childs?')

    @api.multi
    def prepare_inventory(self):
        inventory_line_obj = self.env['stock.inventory.line']
        for inventory in self:
            if inventory.filter == 'ondate':
                operator = 'in'
                if inventory.location_childs:
                    operator = 'child_of'
                history_data = self.env['stock.history'].search(
                    [('date', '<=', inventory.date),
                     ('location_id', operator, [inventory.location_id.id])])
                for product in history_data.mapped('product_id'):
                    lines = history_data.filtered(
                        lambda x: x.product_id == product)
                    for location in lines.mapped('location_id'):
                        llines = lines.filtered(
                            lambda x: x.location_id == location)
                        qty = sum(llines.mapped('quantity'))
                        if qty != 0:
                            inventory_line_obj.create({
                                'inventory_id': inventory.id,
                                'product_id': product.id,
                                'product_qty': qty,
                                'location_id': location.id,
                            })
                inventory.write({'state': 'confirm'})
            else:
                super(StockInventory, inventory).prepare_inventory()
        return True

    @api.multi
    def action_done(self):
        super(StockInventory,
              self.filtered(lambda x: x.filter == 'ondate')).write({
                  'state': 'cancel',
              })
        return super(StockInventory,
                     self.filtered(
                         lambda x: x.filter != 'ondate')).action_done()
