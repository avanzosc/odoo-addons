# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models, api


class QcTest(models.Model):

    _inherit = 'qc.test'

    product_tmpl_id = fields.Many2one(comodel_name='product.template',
                                      string='Template')
    product_id = fields.Many2one(comodel_name='product.product',
                                 string='Product')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner')
    parent_id = fields.Many2one(comodel_name='qc.test', string='Parent')
    no_inspection = fields.Boolean(string='Not allow inspections')

    @api.multi
    @api.onchange('product_id')
    def onchange_product(self):
        self.ensure_one()
        self.product_tmpl_id = self.product_id.product_tmpl_id

    @api.multi
    @api.onchange('parent_id')
    def onchange_parent(self):
        self.ensure_one()
        self.test_lines.unlink()
        self.test_lines = [
            [0, 0, x] for x in self.parent_id.test_lines.copy_data(
                default={'test': False})]
