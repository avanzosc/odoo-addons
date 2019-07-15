# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api, exceptions


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    report_data_ids = fields.One2many(comodel_name='stock.label.report.data',
                                      inverse_name='picking_id',
                                      string='Reports Data')

    @api.multi
    def print_label_report(self):
        if any(self.mapped('report_data_ids').filtered(lambda x: x.ul_qty !=
                                                       x.ul_computed_qty)):
            raise exceptions.Warning('Error! There is some wrong label data.')
        return self.env['report'].get_action(
            self.mapped('report_data_ids'),
            'stock_picking_label_print.stock_label_report')
