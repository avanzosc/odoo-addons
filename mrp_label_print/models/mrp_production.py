# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api, exceptions


class MrpProduction(models.Model):

    _inherit = 'mrp.production'

    report_data_ids = fields.One2many(comodel_name='stock.label.report.data',
                                      inverse_name='production_id',
                                      string='Reports Data')

    @api.multi
    def print_label_report(self):
        if any(self.mapped('report_data_ids').filtered(lambda x: x.ul_qty !=
                                                       x.ul_computed_qty)):
            raise exceptions.Warning('Error! There is some wrong label data.')
        return self.env['report'].get_action(
            self.mapped('report_data_ids'),
            'stock_picking_label_print.stock_label_report')

    @api.model
    def action_produce(self, production_id, production_qty, production_mode,
                       wiz=False):
        report_data_model = self.env['stock.label.report.data']
        production = self.env['mrp.production'].browse(production_id)
        res = super(MrpProduction, self).action_produce(
            production_id, production_qty, production_mode, wiz=wiz)
        if production_mode == 'consume_produce':
            production.report_data_ids.unlink()
            for line in production.move_created_ids2.filtered(
                    lambda x: x.state == 'done'):
                lots = line.mapped('quant_ids.lot_id.id')
                report_data = {
                    'product_id': line.product_id.id,
                    'product_qty': line.product_uom_qty,
                    'ul_id': wiz and wiz.ul_id.id,
                    'ul_qty': wiz and wiz.ul_qty,
                    'lot_id': lots and lots[0] or False,
                    'production_id': production_id,
                }
                report_data_model.create(report_data)
        return res
