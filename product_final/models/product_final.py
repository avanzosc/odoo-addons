# Copyright 2022 Patxi Lersundi 
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.osv import expression
from odoo import api, fields, models


class ProductFinal(models.Model):
    _name= 'product.final'
    _order='code'

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")

    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, '[%s] %s' % (rec.code, rec.name)))
        return result
    
    @api.model
    def _name_search(
#            self, name="", args=None, operator="ilike", limit=100,
            self, name, args=None, operator="ilike", limit=100,
            name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', operator, name), ('name', operator, name)]
        product_final_ids = self._search(expression.AND([domain, args]),
                                    limit=limit, access_rights_uid=name_get_uid)
        return self.browse(product_final_ids).name_get()
