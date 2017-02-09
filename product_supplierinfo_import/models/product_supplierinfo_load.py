# -*- coding: utf-8 -*-
# (c) 2017 Daniel Campos - AvanzOSC
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, exceptions, api, _


class ProductSupplierinfoLoad(models.Model):
    _name = 'product.supplierinfo.load'
    _description = 'Product price list load'

    name = fields.Char(string='Load')
    date = fields.Date(string='Date:', readonly=True)
    file_name = fields.Char(string='File name', readonly=True)
    file_lines = fields.One2many(
        comodel_name='product.supplierinfo.load.line',
        inverse_name='file_load', string='Product price list lines')
    fails = fields.Integer(string='Erroneous lines', readonly=True)
    process = fields.Integer(string='Lines to process:', readonly=True)
    supplier = fields.Many2one(
        comodel_name='res.partner', string='Supplier',
        help="If there is no supplier defined in line this will be used")

    @api.multi
    def process_lines(self):
        for file_load in self:
            partner_obj = self.env['res.partner']
            product_obj = self.env['product.product']
            psupplinfo_obj = self.env['product.supplierinfo']
            pricepinfo_obj = self.env['pricelist.partnerinfo']
            if not file_load.file_lines:
                raise exceptions.Warning(
                    _("There must be one line at least to process"))
            for line in file_load.mapped('file_lines').filtered(
                    lambda x: x.fail and (x.code or x.info)):
                cond = ([('default_code', '=', line.code)] if line.code else
                        [('name', '=', line.info)])
                product = product_obj.search(cond, limit=1)
                supplier = file_load.supplier
                if line.supplier:
                    supplier_lst = partner_obj.search(
                        ['|', ('ref', '=', line.supplier),
                         ('name', "=", line.supplier)], limit=1)
                    supplier = supplier_lst
                if not supplier:
                    line.fail_reason = _('Supplier not found')
                    continue
                if product and supplier:
                    supinfo = product.mapped('seller_ids').filtered(
                        lambda x: x.name.id == supplier.id)
                    vals_supinfo = self._prepare_supinfo_vals(line)
                    if supinfo and vals_supinfo:
                        supinfo.write(vals_supinfo)
                    elif not supinfo:
                        vals_supinfo.update({
                            'name': supplier.id,
                            'product_tmpl_id': product.product_tmpl_id.id})
                        if not vals_supinfo.get('sequence', False):
                            vals_supinfo['sequence'] = 1
                        if not vals_supinfo.get('min_qty', False):
                            vals_supinfo['min_qty'] = 1
                        if not vals_supinfo.get('delay', False):
                            vals_supinfo['delay'] = 1
                        supinfo = psupplinfo_obj.create(vals_supinfo)
                    min_qty = line.min_qty if line.min_qty else supinfo.min_qty
                    pricelist = supinfo.mapped('pricelist_ids').filtered(
                        lambda x: x.min_quantity == min_qty)
                    if pricelist:
                        m = u"<p> Old price: {}, new price: {}, has modified "
                        "for supplier: {}".format(pricelist.price, line.price,
                                                  supplier.name)
                        pricelist.price = line.price
                    else:
                        vals_pricelist = self._prepare_pricelist_vals(
                            supinfo, line)
                        pricepinfo_obj.create(vals_pricelist)
                        m = u"<p> new price: {}, has created for supplier: "
                        "{}".format(line.price, supplier.name)
                    m += "<br> <br>"
                    message_vals = {'type': 'comment',
                                    'model': 'product.product',
                                    'record_name': product.name,
                                    'res_id': product.id,
                                    'body': m}
                    self.env['mail.message'].create(message_vals)
                    file_load.fails -= 1
                    line.write({'fail': False,
                                'fail_reason': _('Correctly Processed')})
                else:
                    line.fail_reason = _('Product not found')
        return True

    def _prepare_supinfo_vals(self, line):
        vals = {}
        if line.sequence:
            vals['sequence'] = line.sequence
        if line.supplier_code:
            vals['product_code'] = line.supplier_code
        if line.supplier_code:
            vals['product_name'] = line.info
        if line.min_qty:
            vals['min_qty'] = line.min_qty
        if line.delay:
            vals['delay'] = line.delay
        return vals

    def _prepare_pricelist_vals(self, supinfo, line):
        vals = {
            'suppinfo_id': supinfo.id,
            'min_quantity': line.min_qty if line.min_qty else supinfo.min_qty,
            'price': line.price}
        return vals


class ProductSupplierinfoLoadLine(models.Model):
    _name = 'product.supplierinfo.load.line'
    _description = 'Product price list load line'

    file_load = fields.Many2one(
        comodel_name='product.supplierinfo.load',
        string='Product price list load', required=True)
    supplier = fields.Char(string='Supplier')
    code = fields.Char(string='Product code')
    sequence = fields.Integer(string='Sequence')
    supplier_code = fields.Char(string='Supplier code')
    info = fields.Char(string='Product description')
    delay = fields.Integer(string='Delivery lead time')
    price = fields.Float(string='Product price', required=True)
    min_qty = fields.Float(string='Minimal quantity')
    fail = fields.Boolean(string='Error')
    fail_reason = fields.Char(string='Reason error')
