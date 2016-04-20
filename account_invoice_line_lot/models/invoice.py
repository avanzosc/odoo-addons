# -*- coding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp import fields, models, api


class AccountInvoiceLine(models.Model):

    @api.one
    def _get_prod_lots(self):
        if self.invoice_id and self.invoice_id.id and self.product_id:
            sale_obj = self.env['sale.order']
            op_obj = self.env['stock.pack.operation']
            sale_lst = sale_obj.search([('invoice_ids', '=',
                                         self.invoice_id.id)])
            pickings = sale_lst.mapped('picking_ids')
            op_lst = op_obj.search([('product_id', '=', self.product_id.id),
                                    ('picking_id', 'in',
                                     pickings.ids)])
            self.prod_lot_ids = op_lst.mapped('lot_id')

    _inherit = "account.invoice.line"

    prod_lot_ids = fields.Many2many(comodel_name="stock.production.lot",
                                    column1="invoice_line_id",
                                    column2="production_lot_id",
                                    relation="invoice_line_lot_rel",
                                    string="Production Lot",
                                    compute="_get_prod_lots")
