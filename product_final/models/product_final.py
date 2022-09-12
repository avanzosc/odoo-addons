# Copyright 2022 Patxi Lersundi
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.osv import expression
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProductFinal(models.Model):
    _name = 'product.final'
    _order = 'code'

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)

    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, '[%s] %s' % (rec.code, rec.name)))
        return result

    @api.model
    def _name_search(
            self, name, args=None, operator="ilike", limit=100,
            name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', operator, name), ('name', operator, name)]
        product_final_ids = self._search(
            expression.AND([domain, args]), limit=limit,
            access_rights_uid=name_get_uid)
        return self.browse(product_final_ids).name_get()

    @api.constrains('code')
    def _check_unique_code(self):
        for final in self:
            cond = [("id", "!=", final.id),
                    ("code", "=", final.code)]
            f = self.env['product.final'].search(cond, limit=1)
            if f:
                raise UserError(
                    _('You are putting the code "%s" to the name "%s", and '
                      'that code already exists for the name "%s".') % (
                          final.code, final.name, f.name))
