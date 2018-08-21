# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    price_unit = fields.Float()
    product_uop_qty = fields.Float(
        string='Quantity (UoP)', readonly=True,
        digits=dp.get_precision('Product UoP'),
        states={'draft': [('readonly', False)]})
    product_uop = fields.Many2one(
        comodel_name='product.uom', string='Product UoP')
    product_uop_coeff = fields.Float(
        comodel_name='product.uom', string='UoM -> UoP Coeff',
        digits=dp.get_precision('Product UoP'))
    price_unit_uop = fields.Float(
        string='UoP Unit Price', readonly=True,
        digits=dp.get_precision('Product Price'),
        states={'draft': [('readonly', False)]})

    @api.onchange('price_unit')
    def onchange_price_unit(self):
        if self.product_id and self.product_id.uop_coeff:
            price = self.env['account.tax']._fix_tax_included_price(
                self.price_unit, self.product_id.supplier_taxes_id,
                self.taxes_id.ids)
            self.price_unit = price
            self.price_unit_uop = price / self.product_id.uop_coeff

    @api.onchange('price_unit_uop')
    def onchange_price_unit_uop(self):
        if self.product_id:
            price = self.env['account.tax']._fix_tax_included_price(
                self.price_unit_uop, self.product_id.supplier_taxes_id,
                self.taxes_id.ids)
            self.price_unit_uop = price
            self.price_unit = price * self.product_uop_coeff

    @api.onchange('product_uop_qty')
    def onchange_product_uop_qty(self):
        if self.product_id:
            self.product_qty = self.product_uop_qty / self.product_uop_coeff

    @api.onchange('product_uop')
    def onchange_product_uop(self):
        if self.product_uop == self.product_id.uop_id:
            self.product_uop_coeff = self.product_uop_coeff
        else:
            # TODO: See if units are of the same category
            self.product_uop_coeff = 1.0

    @api.onchange('product_uop_coeff')
    def onchange_product_uop_coeff(self):
        self.product_uop_qty = self.product_qty * self.product_uop_coeff

    @api.onchange('product_id')
    def onchange_product_id(self):
        result = super(PurchaseOrderLine, self).onchange_product_id()
        self.product_uop = self.product_id.uop_id
        self.product_uop_coeff = self.product_id.uop_coeff
        self.product_uop_qty = self.product_qty * self.product_uop_coeff
        return result

    @api.onchange('product_qty', 'product_uom')
    def _onchange_quantity(self):
        result = super(PurchaseOrderLine, self)._onchange_quantity()
        self.product_uop_qty = self.product_qty * self.product_uop_coeff
        return result

    # @api.multi
    # def onchange_product_id(
    #         self, pricelist_id, product_id, qty, uom_id, partner_id,
    #         date_order=False, fiscal_position_id=False, date_planned=False,
    #         name=False, price_unit=False, state='draft'):
    #     res = super(PurchaseOrderLine, self).onchange_product_id(
    #         pricelist_id, product_id, qty, uom_id, partner_id,
    #         date_order=date_order, fiscal_position_id=fiscal_position_id,
    #         date_planned=date_planned, name=name, price_unit=price_unit,
    #         state=state)
    #     value = res.setdefault('value', {})
    #     if product_id:
    #         product_obj = self.env['product.product']
    #         product = product_obj.browse(product_id)
    #         if product.uop_id:
    #             value['product_uop'] = product.uop_id.id
    #             value['product_uop_qty'] = qty * product.uop_coeff
    #     else:
    #         value['product_uop'] = False
    #         value['product_uop_qty'] = 0.0
    #     return res
