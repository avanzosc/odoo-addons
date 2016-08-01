# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    mrp_production_id = fields.Many2one(
        comodel_name='mrp.production', string='Mrp Production')
    schedule_products = fields.One2many(
        comodel_name='mrp.production.product.line',
        related='mrp_production_id.product_lines')

    @api.multi
    def need_procurement(self):
        for line in self:
            if line.mrp_production_id:
                return False
            else:
                return super(SaleOrderLine, self).need_procurement()

    @api.multi
    def action_create_mrp(self):
        attribute_list = []
        for attribute_line in self.product_attribute_ids:
            attribute_list.append({
                'attribute_id': attribute_line.attribute_id.id,
                'value_id': attribute_line.value_id.id,
                'product_tmpl_id': self.product_tmpl_id.id,
                'owner_model': 'mrp.production',
            })
        mrp = self.env['mrp.production'].create({
            'product_tmpl_id': self.product_tmpl_id.id or False,
            'product_id': self.product_id.id or False,
            'product_qty': self.product_uom_qty,
            'product_uom': self.product_tmpl_id.uom_id.id,
            'product_attribute_ids': [(0, 0, x) for x in attribute_list],
            'sale_line': self.id,
            'sale_order': self.order_id.id,
            'partner': self.order_id.partner_id.id,
            'active': False,
            })
        self.mrp_production_id = mrp
        self.action_compute_products()

    @api.multi
    def action_compute_products(self):
        if self.mrp_production_id:
            self.mrp_production_id.action_compute()


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_button_confirm(self):
        res = super(SaleOrder, self).action_button_confirm()
        lines = self.order_line.filtered(
            lambda x: x.mrp_production_id is not False)
        for line in lines:
            for mrp in line.mrp_production_id:
                mrp.write(
                    {'active': True,
                     'sale_order': self.id,
                     'sale_line': line.id,
                     'partner': self.partner_id.id,
                     'name':
                        self.env['ir.sequence'].get('mrp.production') or '/',
                     })
        return res

    @api.multi
    def action_show_manufacturing_orders(self):
        return {
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'mrp.production',
            'type': 'ir.actions.act_window',
            'search_view_id': self.env.ref(
                'mrp.view_mrp_production_filter').id,
            'domain': "[('sale_order', '=', " + str(self.id) + ")]",
            'context': self.env.context
            }
