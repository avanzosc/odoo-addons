# -*- coding: utf-8 -*-
# Copyright 2019 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.template"

    attachment_qty = fields.Integer(string="Attachments",
                                    compute="count_attachments")

    @api.multi
    def count_attachments(self):
        for product in self:
            product.attachment_qty = self.env['ir.attachment'].search_count(
                [('res_model', '=', self._model._name),
                 ('res_id', '=', product.id)])
