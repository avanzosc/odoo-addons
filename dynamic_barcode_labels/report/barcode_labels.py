# -*- coding: utf-8 -*-
# Copyright (c) 2015-Present TidyWay Software Solution. (<https://tidyway.in/>)

import time

from odoo import models, api, _
from odoo.exceptions import UserError
from reportlab.graphics import barcode
from base64 import b64encode


class ReportBarcodeLabels(models.AbstractModel):
    _name = 'report.dynamic_barcode_labels.report_barcode_labels'

    @api.multi
    def _get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        config = self.env.ref('dynamic_barcode_labels.default_barcode_configuration')
        if not config:
            raise Warning(_(" Please configure barcode data from "
                            "configuration menu"))
        product_obj = self.env["product.product"]
        browse_record_list = []
        for rec in data['form']['product_ids']:
            for loop in range(0, int(rec['qty'])):
                browse_record_list.append((
                       product_obj.browse(int(rec['product_id'])),
                       rec['lot_number']
                       ))
        print(config, config.product_name, config.product_name_size)
        return {
            'doc_ids': data['form']['product_ids'],
            'doc_model': self.env['product.product'],
            'data': data,
            'docs': browse_record_list,
            'get_barcode_value': self.get_barcode_value,
            'is_humanreadable': self.is_humanreadable,
            'time': time,
            'config': config,
            'get_barcode_string': self._get_barcode_string,
        }

    def is_humanreadable(self, data):
        return data['form']['humanreadable'] and 1 or 0

    def get_barcode_value(self, product, data):
        barcode_value = product[str(data['form']['barcode_field'])]
        return barcode_value

#     def _get_barcode_string(self, product, data):
#         barcode_value = product[str(data['form']['barcode_field'])]
#         humanreadable = data['form']['humanreadable'] and 1 or 0
#         print ("'{0}', '{1}', '{2}', '{3}', '{4}'".format(
#                                     data['form']['barcode_type'],
#                                     barcode_value,
#                                     int(data['form']['barcode_height']),
#                                     int(data['form']['barcode_width']),
#                                     humanreadable
#                                     ))
#         return "'{0}', '{1}', '{2}', '{3}', '{4}'".format(
#                                     data['form']['barcode_type'],
#                                     barcode_value,
#                                     int(data['form']['barcode_height']),
#                                     int(data['form']['barcode_width']),
#                                     humanreadable
#                                     )
#         return "('%s','%s',%s,%s,%s)" % (
#                                      data['form']['barcode_type'],
#                                      barcode_value,
#                                      int(data['form']['barcode_height']),
#                                      int(data['form']['barcode_width']),
#                                      humanreadable
#                                      )
# 
    def _get_barcode_string(self, product, data):
        barcode_value = product[str(data['form']['barcode_field'])]
        barcode_str = barcode.createBarcodeDrawing(
                            data['form']['barcode_type'],
                            value=barcode_value,
                            format='png',
                            width=int(data['form']['barcode_height']),
                            height=int(data['form']['barcode_width']),
                            humanReadable=data['form']['humanreadable']
                            )
        encoded_string = b64encode(barcode_str.asString('png'))
        barcode_str = "<img style='width:" + str(data['form']['display_width']) + "px;height:" + str(data['form']['display_height']) + "px'src='data:image/png;base64,{0}'>".format(encoded_string.decode("utf-8"))
        return barcode_str or ''

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
