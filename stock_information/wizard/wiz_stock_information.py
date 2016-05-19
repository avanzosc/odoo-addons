# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, _


class WizStockInformation(models.TransientModel):

    _name = 'wiz.stock.information'
    _description = 'Wizard stock information'

    @api.multi
    def _def_company(self):
        return self.env.user.company_id.id

    company = fields.Many2one(
        'res.company', 'Company', default=_def_company, required=True)
    to_date = fields.Date('To date', required=True,
                          help='Deadline for calculating periods')
    category = fields.Many2one(
        'product.category', 'Category',
        help='Enter this field if you want to filter by category')
    template = fields.Many2one(
        'product.template', 'Template',
        help='Enter this field if you want to filter by template')
    product = fields.Many2one(
        'product.product', 'Product',
        help='Enter this field if you want to filter by product')
    locations = fields.Many2many(
        comodel_name='stock.location', relation='rel_wiz_stock_info_location',
        column1='wiz_stock_info_id', column2='location_id',
        string='Locations')

    @api.multi
    def calculate_stock_information(self):
        self.ensure_one()
        information_obj = self.env['stock.information']
        infor = information_obj.search(self._prepare_information_search())
        infor.unlink()
        to_date = information_obj._calculate_last_day_week(
            fields.Datetime.from_string(self.to_date).date())
        products = []
        if self.product:
            products = [self.product.id]
        product_datas = self._cath_moves_and_procurements(to_date, products)
        information_obj._generate_stock_information(self, product_datas)
        return {'name': _('Stock information'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree',
                'res_model': 'stock.information'}

    def _prepare_information_search(self):
        cond = [('company', '=', self.company.id)]
        if self.category:
            cond.append(('category', '=', self.category.id))
        if self.template:
            cond.append(('product_template', '=', self.template.id))
        if self.product:
            cond.append(('product', 'in', [self.product.id]))
        if self.locations:
            cond.append(('location', 'in', self.locations.ids))
        return cond

    def _cath_moves_and_procurements(self, to_date, products):
        move_obj = self.env['stock.move']
        proc_obj = self.env['procurement.order']
        product_datas = {}
        for move in move_obj._find_moves_from_stock_information(
            self.company, to_date, category=self.category,
                template=self.template, products=products):
            if move.location_id.usage == 'internal':
                if (not self.locations or
                    (self.locations and move.location_id.id in
                     self.locations.ids)):
                    product_datas = self._find_product_in_table(
                        product_datas, move.product_id, move.location_id)
            if move.location_dest_id.usage == 'internal':
                if (not self.locations or
                    (self.locations and move.location_dest_id.id in
                     self.locations.ids)):
                    product_datas = self._find_product_in_table(
                        product_datas, move.product_id, move.location_dest_id)
        for procurement in proc_obj._find_procurements_from_stock_information(
            self.company, to_date, category=self.category,
                template=self.template, products=products):
            if (not self.locations or
                (self.locations and procurement.location_id.id in
                 self.locations.ids)):
                product_datas = self._find_product_in_table(
                    product_datas, procurement.product_id,
                    procurement.location_id)
        return product_datas

    def _find_product_in_table(self, product_datas, product, location):
        found = False
        for data in product_datas:
            datos_array = product_datas[data]
            dproduct = datos_array['product']
            dlocation = datos_array['location']
            if dproduct.id == product.id and dlocation.id == location.id:
                found = True
        if not found:
            my_vals = {'product': product,
                       'location': location}
            ind = product.id + location.id
            product_datas[(ind)] = my_vals
        return product_datas
