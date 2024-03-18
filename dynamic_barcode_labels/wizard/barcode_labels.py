# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2015-Present TidyWay Software Solution. (<https://tidyway.in/>)
#
#################################################################################

from odoo import models, fields, api, _
from odoo.exceptions import Warning
from reportlab.graphics import barcode


class BarcodeProductLines(models.TransientModel):
    _name = "barcode.product.lines"

    product_id = fields.Many2one(
         'product.product',
         string='Product',
         required=True
         )
    lot_id = fields.Many2one(
         'stock.production.lot',
         string='Production Lot'
         )
    qty = fields.Integer(
         'Barcode Labels Qty',
         default=1,
         required=True
         )
    wizard_id = fields.Many2one(
        'barcode.labels',
        string='Wizard'
        )

    @api.onchange('product_id')
    def onchange_product(self):
        if not self.product_id.id:
            return {}
        return {
                  'domain':
                            {
                             'lot_id': [('product_id', '=', self.product_id.id)]
                             },
                }

    @api.onchange('lot_id')
    def onchange_lot(self):
        if not self.lot_id:
            return {}
        self.qty = self.lot_id.product_qty or 0.0


class BarcodeLabels(models.TransientModel):
    _name = "barcode.labels"
    _description = 'Barcode Labels'

    @api.model
    def default_get(self, fields):
        product_get_ids = []
        if self._context.get('active_model') == 'product.product':
            record_ids = self._context.get('active_ids', []) or []
            products = self.env['product.product'].browse(record_ids)
            product_get_ids = [(0, 0, {
                                     'product_id': product.id,
                                     'qty': 1.0
                                     }) for product in products]
        elif self._context.get('active_model') == 'product.template':
            record_ids = self._context.get('active_ids', []) or []
            templates = self.env['product.template'].browse(record_ids)
            product_get_ids = []
            for template in templates:
                product_get_ids += [(0, 0, {
                             'product_id': product.id,
                             'qty': 1.0
                             }) for product in template.product_variant_ids]
        elif self._context.get('active_model') == 'purchase.order':
            record_ids = self._context.get('active_ids', []) or []
            purchase_recs = self.env['purchase.order'].browse(record_ids)
            product_get_ids = []
            for purchase in purchase_recs:
                for line in purchase.order_line:
                    if line.product_id and line.product_id.type != 'service':
                        product_get_ids += [(0, 0, {
                                 'product_id': line.product_id.id,
                                 'qty': int(abs(line.product_qty)) or 1.0
                                 })]
        elif self._context.get('active_model') == 'stock.picking':
            record_ids = self._context.get('active_ids', []) or []
            picking_recs = self.env['stock.picking'].browse(record_ids)
            product_get_ids = []
            for picking in picking_recs:
                for line in picking.move_lines:
                    if line.product_id and line.product_id.type != 'service':
                        product_get_ids += [(0, 0, {
                                 'product_id': line.product_id.id,
                                 'qty': int(abs(line.product_qty)) or 1.0
                                 })]
        view_id = self.env['ir.ui.view'].search([('name', '=', 'report_barcode_labels')])
        if not view_id.arch:
            raise Warning('Someone has deleted the reference '
                          'view of report, Please Update the module!')
        return {
                'product_get_ids': product_get_ids
                }

    product_get_ids = fields.One2many(
          'barcode.product.lines',
          'wizard_id',
          string='Products'
          )

    @api.model
    def _create_paper_format(self, data):
        report_action_id = self.env['ir.actions.report'].sudo().search([('report_name', '=', 'dynamic_barcode_labels.report_barcode_labels')])
        if not report_action_id:
            raise Warning('Someone has deleted the reference view of report, Please Update the module!')
        config_rec = self.env['barcode.configuration'].search([], limit=1)
        if not config_rec:
            raise Warning(_(" Please configure barcode data from "
                            "configuration menu"))
        page_height = config_rec.label_height or 10
        page_width = config_rec.label_width or 10
        margin_top = config_rec.margin_top or 1
        margin_bottom = config_rec.margin_bottom or 1
        margin_left = config_rec.margin_left or 1
        margin_right = config_rec.margin_right or 1
        dpi = config_rec.dpi or 90
        header_spacing = config_rec.header_spacing or 1
        orientation = 'Portrait'
        self._cr.execute(""" DELETE FROM report_paperformat WHERE custom_report=TRUE""")
        paperformat_id = self.env['report.paperformat'].sudo().create({
                'name': 'Custom Report',
                'format': 'custom',
                'page_height': page_height,
                'page_width': page_width,
                'dpi': dpi,
                'custom_report': True,
                'margin_top': margin_top,
                'margin_bottom': margin_bottom,
                'margin_left': margin_left,
                'margin_right': margin_right,
                'header_spacing': header_spacing,
                'orientation': orientation,
                #'display_height': config_rec.display_height,
                #'display_width': config_rec.display_width,
                #'humanreadable': config_rec.humanreadable,
                #'lot': config_rec.lot
                })
        report_action_id.sudo().write({'paperformat_id': paperformat_id.id})
        return True

    @api.multi
    def print_report(self):
        if not self.env.user.has_group('dynamic_barcode_labels.group_barcode_labels'):
            raise Warning(_("You have not enough rights to access this "
                            "document.\n Please contact administrator to access "
                            "this document."))
        if not self.product_get_ids:
            raise Warning(_(""" There is no product lines to print."""))
        config_rec = self.env['barcode.configuration'].search([], limit=1)
        if not config_rec:
            raise Warning(_(" Please configure barcode data from "
                            "configuration menu"))
        datas = {
                 'ids': [x.product_id.id for x in self.product_get_ids],
                 'model': 'product.product',
                 'form': {
                    'label_width': config_rec.label_width or 50,
                    'label_height': config_rec.label_height or 50,
                    'margin_top': config_rec.margin_top or 1,
                    'margin_bottom': config_rec.margin_bottom or 1,
                    'margin_left': config_rec.margin_left or 1,
                    'margin_right': config_rec.margin_right or 1,
                    'dpi': config_rec.dpi or 90,
                    'header_spacing': config_rec.header_spacing or 1,
                    'barcode_height': config_rec.barcode_height or 300,
                    'barcode_width': config_rec.barcode_width or 1500,
                    'barcode_type': config_rec.barcode_type or 'EAN13',
                    'barcode_field': config_rec.barcode_field or '',
                    'display_width': config_rec.display_width,
                    'display_height': config_rec.display_height,
                    'humanreadable': config_rec.humanreadable,
                    'product_name': config_rec.product_name,
                    'product_variant': config_rec.product_variant,
                    'price_display': config_rec.price_display,
                    'lot': config_rec.lot,
                    'product_code': config_rec.product_code or '',
                    'barcode': config_rec.barcode,
                    'currency_position': config_rec.currency_position or 'after',
                    'currency': config_rec.currency and config_rec.currency.id or '',
                    'symbol': config_rec.currency and config_rec.currency.symbol or '',
                    'product_ids': [{
                         'product_id': line.product_id.id,
                         'lot_id': line.lot_id and line.lot_id.id or False,
                         'lot_number': line.lot_id and line.lot_id.name or False,
                         'qty': line.qty,
                         } for line in self.product_get_ids]
                      }
                 }
        browse_pro = self.env['product.product'].browse([x.product_id.id for x in self.product_get_ids])
        for product in browse_pro:
            barcode_value = product[config_rec.barcode_field]
            if not barcode_value:
                raise Warning(_('Please define barcode for %s!' % (product['name'])))
            try:
                barcode.createBarcodeDrawing(
                            config_rec.barcode_type,
                            value=barcode_value,
                            format='png',
                            width=int(config_rec.barcode_height),
                            height=int(config_rec.barcode_width),
                            humanReadable=config_rec.humanreadable or False
                            )
            except:
                raise Warning('Select valid barcode type according barcode field value or check value in field!')

        self.sudo()._create_paper_format(datas['form'])
        return self.env.ref('dynamic_barcode_labels.barcodelabels').report_action([], data=datas)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
