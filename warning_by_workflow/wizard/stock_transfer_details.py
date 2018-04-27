# -*- coding: utf-8 -*-
# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class StockTransferDetails(models.TransientModel):
    _inherit = 'stock.transfer_details'

    partner_warning = fields.Html(string='Warning')

    @api.model
    def default_get(self, fields):
        res = super(StockTransferDetails, self).default_get(fields)
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids')
        partners = self.env[active_model].browse(active_ids).mapped(
            'partner_id')
        messages = []
        for partner in partners:
            level, warn_msg = partner._get_warning_message('picking_warn')
            string = (
                u'<b>{}</b>:<br/><span style="color:green;font-size:20px;">{'
                u'}</span>'
                if level != 'block' else
                u'<b>{}</b>:<br/><span style="color:red;font-size:25px">{'
                u'}</span>')
            messages.append(string.format(partner.name, warn_msg))
        res.update({'partner_warning': '<br/>'.join(messages)})
        return res
