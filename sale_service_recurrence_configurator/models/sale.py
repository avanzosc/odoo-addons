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
        quote_obj = self.env['sale.quote.line']
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
                template = quote_obj.search(cond)
                if len(template) > 1:
                    cond = [('quote_id', '=', template_id),
                            ('product_template', '!=', False),
                            ('product_id', '=', False),
                            ('name', '=', dic.get('name'))]
                    template = quote_obj.search(cond, limit=1)
                line = self._sale_line_with_sale_quote_information(
                    template, line)
                if template.product_id:
                    line[2].update({'product_id': template.product_id.id})
        return res

    @api.multi
    def _sale_line_with_sale_quote_information(self, template, line):
        line[2].update({
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
            'week6': template.week6,
            'monday': template.monday,
            'tuesday': template.tuesday,
            'wednesday': template.wednesday,
            'thursday': template.thursday,
            'friday': template.friday,
            'saturday': template.saturday,
            'sunday': template.sunday})
        return line


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
    week6 = fields.Boolean('Week 6')
    monday = fields.Boolean('Monday')
    tuesday = fields.Boolean('Tuesday')
    wednesday = fields.Boolean('Wednesday')
    thursday = fields.Boolean('Thursday')
    friday = fields.Boolean('Friday')
    saturday = fields.Boolean('Saturday')
    sunday = fields.Boolean('Sunday')


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
    week6 = fields.Boolean('Week 6')
    monday = fields.Boolean('Monday')
    tuesday = fields.Boolean('Tuesday')
    wednesday = fields.Boolean('Wednesday')
    thursday = fields.Boolean('Thursday')
    friday = fields.Boolean('Friday')
    saturday = fields.Boolean('Saturday')
    sunday = fields.Boolean('Sunday')

    @api.multi
    @api.onchange('product_template')
    def onchange_product_template(self):
        self.ensure_one()
        if not self.product_template:
            self.product_id = False
        else:
            self.product_uom_id = self.product_template.uom_id.id
            self.name = self.product_template.name
            if not self.product_template.attribute_line_ids:
                self.product_id = (
                    self.product_template.product_variant_ids and
                    self.product_template.product_variant_ids[0])
            return {'domain': {'product_id': [('product_tmpl_id', '=',
                                               self.product_template.id)]}}

    @api.multi
    def on_change_product_id(self, product):
        result = super(SaleQuoteLine, self).on_change_product_id(product)
        if 'value' in result and product:
            prod = self.env['product.product'].browse(product)
            result['value']['product_template'] = prod.product_tmpl_id.id
        return result
