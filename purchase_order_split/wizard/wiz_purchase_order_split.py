# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api, exceptions, _
from dateutil.relativedelta import relativedelta
from datetime import datetime


class WizPurchaseOrderSplit(models.TransientModel):
    _name = 'wiz.purchase.order.split'
    _description = '"Wizard to split purchase order'

    parts = fields.Integer(
        string='How many parts', required=True,
        help='Purchase order number to split the purchase order')
    from_date = fields.Date(
        string='From date', required=True,
        help='Expected date on which the first purchase order begins')
    each_month = fields.Integer(
        string='Each how many month', required=True,
        help='Months interval to generate each purchase order')

    @api.multi
    def action_split_purchase_order(self):
        self.ensure_one()
        pur_obj = self.env['purchase.order']
        for purchase in pur_obj.browse(self.env.context.get('active_ids')):
            origin = purchase.origin or False
            date_order = purchase.date_order
            if purchase.state != 'draft':
                raise exceptions.Warning(
                    _('Purchase order: %s not in draft state') %
                    (purchase.name))
            for line in purchase.order_line:
                x = line.product_qty % self.parts
                if x != 0:
                    raise exceptions.Warning(
                        _("The amount %s of the sale order line of purchase"
                          " order: '%s', with product: '%s', can not divide"
                          " by: %s") % (str(line.product_qty), purchase.name,
                                        line.product_id.name, str(self.parts)))
                line.product_qty = line.product_qty / self.parts
            first_date = datetime.strptime(self.from_date, '%Y-%m-%d').date()
            new_purchase = purchase
            month_count = self.parts
            while month_count > 1:
                next_date = first_date + relativedelta(months=self.each_month)
                new_purchase.minimum_planned_date = next_date
                new_purchase = new_purchase.copy()
                vals = {'date_order': date_order}
                if origin:
                    vals.update({'origin': origin})
                new_purchase.write(vals)
                first_date = datetime.strptime(
                    str(next_date), '%Y-%m-%d').date()
                month_count -= 1
            next_date = first_date + relativedelta(months=self.each_month)
            new_purchase.minimum_planned_date = next_date
