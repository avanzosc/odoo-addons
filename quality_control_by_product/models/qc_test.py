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
    template_trigger_line_ids = fields.One2many(
        comodel_name='qc.trigger.product_template_line', inverse_name='test',
        string='Template Trigger Lines')
    product_trigger_line_ids = fields.One2many(
        comodel_name='qc.trigger.product_line', inverse_name='test',
        string='Product Trigger Lines')
    has_trigger_lines = fields.Boolean(string="Has Trigger Lines",
                                       compute="_compute_has_trigger_lines")

    @api.multi
    @api.depends('template_trigger_line_ids', 'product_trigger_line_ids')
    def _compute_has_trigger_lines(self):
        for record in self:
            record.has_trigger_lines = bool(record.product_trigger_line_ids or
                                            record.template_trigger_line_ids)

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

    @api.multi
    def create_trigger_line(self, trigger):
        product_trigger_line_obj = self.env['qc.trigger.product_line']
        tmpl_trigger_line_obj = self.env['qc.trigger.product_template_line']
        for record in self.filtered(lambda x: x.product_id or
                                    x.product_tmpl_id):
            values = {'test': record.id,
                      'user': self.env.user.id,
                      'trigger': trigger.id
                      }
            if record.partner_id:
                values.update({'partners': [(6, 0, [record.partner_id.id])]})
            if record.product_id:
                values.update({'product': record.product_id.id})
                product_trigger_line_obj.create(values)
            elif record.product_tmpl_id:
                values.update({'product_template': record.product_tmpl_id.id})
                tmpl_trigger_line_obj.create(values)
