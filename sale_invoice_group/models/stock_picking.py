# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    @api.one
    @api.depends('date_done', 'partner_id')
    def _get_inv_exp_date(self):
        value = False
        if self.partner_id.invoicing_group:
            if self.date_done:
                delay = self.partner_id.invoicing_group.delay
                date_format = "%Y-%m-%d %H:%M:%S"
                date_done = datetime.strptime(self.date_done, date_format)
                value = date_done + relativedelta(days=delay)
        self.invoicing_exp_date = value

    invoicing_exp_date = fields.Date(string="Invoicing Expected Date",
                                     compute=_get_inv_exp_date, store=True)

    def action_invoice_create(self, cr, uid, ids, journal_id, group=False,
                              type='out_invoice', context=None):
        inv_date = context.get('date_inv', False)
        if not inv_date:
            inv_date = datetime.now()
        picking_ids = self.search(cr, uid, [('id', 'in', ids), '|',
                                            ('invoicing_exp_date', '<=',
                                             inv_date),
                                            ('invoicing_exp_date', '=',
                                             False)],
                                  context=context)
        result = super(StockPicking, self).action_invoice_create(
            cr, uid, picking_ids, journal_id, group=True, type=type,
            context=context)
        return result
