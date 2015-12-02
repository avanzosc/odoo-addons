# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models
from openerp.osv import expression


class CrmCaseCateg(models.Model):
    _inherit = 'crm.case.categ'

    parent_id = fields.Many2one(
        comodel_name='crm.case.categ', string='Parent category', select=True)
    complete_name = fields.Char(
        string='Name', compute='_compute_complete_name')

    def check_recursion(self, cr, uid, ids, context=None, parent=None):
        return super(CrmCaseCateg, self)._check_recursion(
            cr, uid, ids, context=context, parent=parent)

    @api.multi
    def name_get(self):
        def get_names(cat):
            """ Return the list [cat.name, cat.parent_id.name, ...] """
            res = []
            while cat:
                res.append(cat.name)
                cat = cat.parent_id
            return res

        return [(cat.id, " / ".join(reversed(get_names(cat)))) for cat in self]

    def name_search(self, cr, uid, name, args=None, operator='ilike',
                    context=None, limit=100):
        if not args:
            args = []
        if not context:
            context = {}
        if name:
            # Be sure name_search is symetric to name_get
            categories = name.split(' / ')
            parents = list(categories)
            child = parents.pop()
            domain = [('name', operator, child)]
            if parents:
                names_ids = self.name_search(
                    cr, uid, ' / '.join(parents), args=args, operator='ilike',
                    context=context, limit=limit)
                category_ids = [name_id[0] for name_id in names_ids]
                if operator in expression.NEGATIVE_TERM_OPERATORS:
                    category_ids = self.search(
                        cr, uid, [('id', 'not in', category_ids)])
                    domain = expression.OR(
                        [[('parent_id', 'in', category_ids)], domain])
                else:
                    domain = expression.AND(
                        [[('parent_id', 'in', category_ids)], domain])
                for i in range(1, len(categories)):
                    domain = [[('name', operator,
                                ' / '.join(categories[-1 - i:]))], domain]
                    if operator in expression.NEGATIVE_TERM_OPERATORS:
                        domain = expression.AND(domain)
                    else:
                        domain = expression.OR(domain)
            ids = self.search(cr, uid, expression.AND([domain, args]),
                              limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
        return self.name_get(cr, uid, ids, context)

    @api.multi
    def _compute_complete_name(self):
        for categ in self:
            categ.complete_name = categ.name_get()[0][1]

    _constraints = [
        (check_recursion,
         'Error ! You cannot create recursive categories of case.',
         ['parent_id'])
    ]
