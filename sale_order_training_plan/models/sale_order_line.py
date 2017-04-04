# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    training = fields.Text(string='Training')

    @api.multi
    def product_id_change(
            self, pricelist, product, qty=0, uom=False, qty_uos=0, uos=False,
            name='', partner_id=False, lang=False, update_tax=True,
            date_order=False, packaging=False, fiscal_position=False,
            flag=False):
        product_obj = self.env['product.product']
        res = super(SaleOrderLine, self).product_id_change(
            pricelist, product, qty=qty, uom=uom, qty_uos=qty_uos, uos=uos,
            name=name, partner_id=partner_id, lang=lang, update_tax=update_tax,
            date_order=date_order, packaging=packaging,
            fiscal_position=fiscal_position, flag=flag)
        if product:
            p = product_obj.browse(product)
            training = ''
            if p.product_training_ids:
                training = self._generate_training_plan_info(
                    p.product_training_ids)
            elif p.product_tmpl_id.product_template_training_ids:
                training = self._generate_training_plan_info(
                    p.product_tmpl_id.product_template_training_ids)
            res['value'].update({'training': training})
        return res

    @api.multi
    def _generate_training_plan_info(self, templates):
        line = ''
        for template in templates:
            line += u'{}.- {}: {}.\n\n'.format(
                    template.sequence, template.training_plan_id.name,
                    template.training_plan_id.planification)
        return line
