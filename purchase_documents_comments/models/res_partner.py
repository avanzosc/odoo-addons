# -*- coding: utf-8 -*-
# Copyright 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    purchase_comment = fields.Text(
        string='Comments for purchase orders')
    purchase_propagated_comment = fields.Text(
        string='Propagated comments for purchase orders')
    in_picking_comment = fields.Text(
        string='Comments for supplier pickings')
    in_picking_propagated_comment = fields.Text(
        string='Propagated comments for supplier pickings')
    in_invoice_comment = fields.Text(
        string='Comments for supplier invoices')

    def _get_purchase_comments(self):
        comment_list = []
        pcomment_list = []
        if self.purchase_comment:
            comment_list.append(self.purchase_comment)
        if self.parent_id.purchase_comment:
            comment_list.append(self.parent_id.purchse_comment)
        if self.purchase_propagated_comment:
            pcomment_list.append(self.purchase_propagated_comment)
        if self.parent_id.purchase_propagated_comment:
            pcomment_list.append(self.parent_id.purchase_propagated_comment)
        return '\n'.join(comment_list), '\n'.join(pcomment_list)

    def _get_supplier_picking_comments(self):
        comment_list = []
        pcomment_list = []
        if self.in_picking_comment:
            comment_list.append(self.in_picking_comment)
        if self.parent_id.in_picking_comment:
            comment_list.append(self.parent_id.in_picking_comment)
        if self.in_picking_propagated_comment:
            pcomment_list.append(self.in_picking_propagated_comment)
        if self.parent_id.in_picking_propagated_comment:
            pcomment_list.append(self.parent_id.in_picking_propagated_comment)
        return '\n'.join(comment_list), '\n'.join(pcomment_list)

    def _get_supplier_invoice_comments(self):
        comment_list = []
        if self.in_invoice_comment:
            comment_list.append(self.in_invoice_comment)
        if self.parent_id.in_invoice_comment:
            comment_list.append(self.parent_id.in_invoice_comment)
        return '\n'.join(comment_list)
