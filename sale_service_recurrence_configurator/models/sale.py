# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def onchange_template_id(self, template_id, partner=False,
                             fiscal_position=False):
        res = super(SaleOrder, self).onchange_template_id(
            template_id, partner=partner, fiscal_position=fiscal_position)
        if (template_id and res.get('value', False) and
                res.get('value')['order_line']):
            res = self._catch_month_week_day_information(template_id, res)
        return res

    def _catch_month_week_day_information(self, template_id, res):
        order_lines = res.get('value')['order_line']
        for line in order_lines:
            if len(line) > 1:
                dic = line[2]
                cond = [('quote_id', '=', template_id)]
                price_unit = dic.get('price_unit', False)
                if price_unit:
                    cond.append(('price_unit', '=', price_unit))
                discount = dic.get('discount', False)
                if discount:
                    cond.append(('discount', '=', discount))
                product_uom_qty = dic.get('product_uom_qty', False)
                if product_uom_qty:
                    cond.append(('product_uom_qty', '=', product_uom_qty))
                product_id = dic.get('product_id', False)
                if product_id:
                    cond.append(('product_id', '=', product_id))
                product_uom = dic.get('product_uom', False)
                if product_uom:
                    cond.append(('product_uom_id', '=', product_uom))
                website_description = dic.get('website_description', False)
                if website_description:
                    cond.append(('website_description', '=',
                                 website_description))
                template = self.env['sale.quote.line'].search(cond)
                line[2].update({
                    'product_tmpl_id': template.product_template.id,
                    'january': template.january,
                    'february': template.february,
                    'march': template.march,
                    'april': template.april,
                    'may': template.may,
                    'june': template.june,
                    'july': template.july,
                    'august': template.august,
                    'september': template.september,
                    'november': template.november,
                    'december': template.december,
                    'week1': template.week1,
                    'week2': template.week2,
                    'week3': template.week3,
                    'week4': template.week4,
                    'week5': template.week5,
                    'monday': template.monday,
                    'tuesday': template.tuesday,
                    'wednesday': template.wednesday,
                    'thursday': template.thursday,
                    'friday': template.friday,
                    'saturday': template.saturday,
                    'sunday': template.sunday})
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    recurring_service = fields.Boolean(
        string='Recurring Service', related='product_id.recurring_service')
    january = fields.Boolean('January')
    february = fields.Boolean('February')
    march = fields.Boolean('March')
    april = fields.Boolean('April')
    may = fields.Boolean('May')
    june = fields.Boolean('June')
    july = fields.Boolean('July')
    august = fields.Boolean('August')
    september = fields.Boolean('September')
    october = fields.Boolean('October')
    november = fields.Boolean('November')
    december = fields.Boolean('December')
    week1 = fields.Boolean('Week 1')
    week2 = fields.Boolean('Week 2')
    week3 = fields.Boolean('Week 3')
    week4 = fields.Boolean('Week 4')
    week5 = fields.Boolean('Week 5')
    monday = fields.Boolean('Monday')
    tuesday = fields.Boolean('Tuesday')
    wednesday = fields.Boolean('Wednesday')
    thursday = fields.Boolean('Thursday')
    friday = fields.Boolean('Friday')
    saturday = fields.Boolean('Saturday')
    sunday = fields.Boolean('Sunday')

    @api.multi
    @api.onchange('product_tmpl_id')
    def onchange_product_tmpl_id(self):
        self.ensure_one()
        if ((self.product_tmpl_id and not self.product_id) or
            (self.product_tmpl_id and self.product_id and
             self.product_tmpl_id.id != self.product_id.product_tmpl_id.id)):
            self.january = False
            self.february = False
            self.march = False
            self.april = False
            self.may = False
            self.june = False
            self.july = False
            self.august = False
            self.september = False
            self.october = False
            self.november = False
            self.december = False
            self.week1 = False
            self.week2 = False
            self.week3 = False
            self.week4 = False
            self.week5 = False
            self.monday = False
            self.tuesday = False
            self.wednesday = False
            self.thursday = False
            self.friday = False
            self.saturday = False
            self.sunday = False
            self.product_id = False
        if self.product_tmpl_id:
            return {'domain': {'product_id': [('product_tmpl_id', '=',
                                               self.product_tmpl_id.id)]}}


class SaleQuoteLine(models.Model):
    _inherit = 'sale.quote.line'

    product_id = fields.Many2one(required=False)
    product_template = fields.Many2one(
        comodel_name='product.template', string='Product Template')
    january = fields.Boolean('January')
    february = fields.Boolean('February')
    march = fields.Boolean('March')
    april = fields.Boolean('April')
    may = fields.Boolean('May')
    june = fields.Boolean('June')
    july = fields.Boolean('July')
    august = fields.Boolean('August')
    september = fields.Boolean('September')
    october = fields.Boolean('October')
    november = fields.Boolean('November')
    december = fields.Boolean('December')
    week1 = fields.Boolean('Week 1')
    week2 = fields.Boolean('Week 2')
    week3 = fields.Boolean('Week 3')
    week4 = fields.Boolean('Week 4')
    week5 = fields.Boolean('Week 5')
    monday = fields.Boolean('Monday')
    tuesday = fields.Boolean('Tuesday')
    wednesday = fields.Boolean('Wednesday')
    thursday = fields.Boolean('Thursday')
    friday = fields.Boolean('Friday')
    saturday = fields.Boolean('Saturday')
    sunday = fields.Boolean('Sunday')

    @api.multi
    def on_change_product_id(self, product):
        self.ensure_one()
        result = super(SaleQuoteLine, self). on_change_product_id(product)
        if 'value' in result and product:
            prod = self.env['product.product'].browse(product)
            result['value']['product_template'] = prod.product_tmpl_id.id
        return result
