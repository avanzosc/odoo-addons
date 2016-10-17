# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models, api
import openerp.addons.decimal_precision as dp


class MrpProductProduceLine(models.TransientModel):

    _inherit = "mrp.product.produce.line"

    inverse_produce_id = fields.Many2one(
        comodel_name='inverse.mrp.product.produce',
        string='Inverse production')


class InverseMrpProductProduce(models.TransientModel):

    _name = "inverse.mrp.product.produce"

    @api.multi
    @api.depends('product_qty', 'consume_lines', 'consume_lines.product_qty')
    def _compute_need_confirm(self):
        for record in self:
            record.need_confirm = False
            if record.product_qty != sum(
                    record.consume_lines.mapped('product_qty')):
                record.need_confirm = True

    product_id = fields.Many2one(comodel_name='product.product',
                                 string='Product to consume',
                                 default=lambda x: x._get_product())
    product_qty = fields.Float(
        string='Select Quantity', required=True,
        digits=dp.get_precision('Product Unit of Measure'),
        default=lambda self: self._get_product_qty())
    mode = fields.Selection([('consume_produce', 'Consume & Produce'),
                             ('consume', 'Consume Only')], string='Mode',
                            default='consume_produce')
    consume_lines = fields.One2many(
        comodel_name='mrp.product.produce.line',
        inverse_name='inverse_produce_id', string='Products Consumed',
        default=lambda self: self._get_lines())
    need_confirm = fields.Boolean(string="Need Confirm",
                                  compute="_compute_need_confirm")

    @api.model
    def _get_lines(self):
        prod_obj = self.env["mrp.production"]
        prod = prod_obj.browse(self.env.context.get('active_id', False))
        new_consume_lines = []
        for line in prod.move_created_ids:
            consume = {'product_id': line.product_id.id,
                       'product_qty': line.product_uom_qty}
            new_consume_lines.append([0, 0, consume])
        return new_consume_lines

    @api.model
    def _get_product_qty(self):
        prod = self.env['mrp.production'].browse(
            self.env.context.get('active_id'))
        done = sum(
            [x.product_uom_qty for x in prod.move_lines2.filtered(
             lambda x: x.product_id == prod.product_id and x.state == 'done')])
        return prod.product_qty - done

    @api.model
    def _get_product(self):
        prod = self.env['mrp.production'].browse(
            self.env.context.get("active_id"))
        return prod and prod.product_id.id or False

    @api.multi
    def do_produce(self):
        production = self.env['mrp.production'].browse(
            self.env.context.get('active_id', False))
        assert production, "Production Id should be specified in context " \
            "as a Active ID."
        production.action_inverse_produce(self)
