# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields
from odoo.tools.float_utils import float_round


class ProductSupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    qty_available = fields.Float(
        string="Quantity On Hand", digits="Product Unit of Measure",
        compute="_compute_supplierinfo_quantities")
    incoming_qty = fields.Float(
        string="Incoming", digits="Product Unit of Measure",
        compute="_compute_supplierinfo_quantities")
    outgoing_qty = fields.Float(
        string="Outgoing", digits="Product Unit of Measure",
        compute="_compute_supplierinfo_quantities")
    comsumed_last_twelve_months = fields.Float(
        string="Consumed last twelve months", digits="Product Unit of Measure",
        compute="_compute_supplierinfo_quantities")
    months_with_stock = fields.Integer(
        string="Months with stock", compute="_compute_supplierinfo_quantities")
    supplier_pending_to_receive = fields.Float(
        string="Pending receipt from supplier",
        compute="_compute_supplier_pending_to_receive")

    def _compute_supplierinfo_quantities(self):
        for supplierinfo in self:
            supplierinfo.qty_available = (
                supplierinfo.product_id.qty_available if
                supplierinfo.product_id else
                supplierinfo.product_tmpl_id.qty_available)
            supplierinfo.incoming_qty = (
                supplierinfo.product_id.incoming_qty if
                supplierinfo.product_id else
                supplierinfo.product_tmpl_id.incoming_qty)
            supplierinfo.outgoing_qty = (
                supplierinfo.product_id.outgoing_qty if
                supplierinfo.product_id else
                supplierinfo.product_tmpl_id.outgoing_qty)
            supplierinfo.comsumed_last_twelve_months = (
                supplierinfo.product_id.comsumed_last_twelve_months if
                supplierinfo.product_id else
                supplierinfo.product_tmpl_id.comsumed_last_twelve_months)
            supplierinfo.months_with_stock = (
                supplierinfo.product_id.months_with_stock if
                supplierinfo.product_id else
                supplierinfo.product_tmpl_id.months_with_stock)

    def _compute_supplier_pending_to_receive(self):
        stock_move_obj = self.env["stock.move"]
        for supplierinfo in self:
            move_lines = stock_move_obj
            pending_to_receive = 0
            cond = [
                ("state", "not in", ("done", "draft", "cancel")),
                ("partner_id", "!=", False),
                ("partner_id", "=", supplierinfo.name.id),
                ("location_id", "!=", False),
                ("location_id.usage", "=", "supplier"),
            ]
            if supplierinfo.product_id:
                cond.append(("product_id", "=", supplierinfo.product_id.id))
            else:
                cond.append(
                    ("product_id.product_tmpl_id", "=",
                     supplierinfo.product_tmpl_id.id))
            movelines = stock_move_obj.search(cond)
            if movelines:
                for move_line in movelines:
                    if move_line not in move_lines:
                        move_lines += move_line
            cond = [
                ("state", "not in", ("done", "draft", "cancel")),
                ("partner_id", "=", False),
                ("picking_id", '!=', False),
                ("picking_id.partner_id", "=", supplierinfo.name.id),
                ("location_id", "!=", False),
                ("location_id.usage", "=", "supplier"),
            ]
            if supplierinfo.product_id:
                cond.append(("product_id", "=", supplierinfo.product_id.id))
            else:
                cond.append(
                    ("product_id.product_tmpl_id", "=",
                     supplierinfo.product_tmpl_id.id))
            movelines = stock_move_obj.search(cond)
            if movelines:
                for move_line in movelines:
                    if move_line not in move_lines:
                        move_lines += move_line
            domain = []
            if move_lines:
                domain = [("id", "in", move_lines.ids)]
            move_lines = stock_move_obj.read_group(
                domain, ['product_id', 'product_uom_qty'], ['product_id'])
            move_data = dict(
                [(data['product_id'][0], data['product_uom_qty'])
                    for data in move_lines])
            if supplierinfo.product_id and supplierinfo.product_id.uom_id:
                pending_to_receive = float_round(
                    move_data.get(supplierinfo.product_id.id, 0),
                    precision_rounding=supplierinfo.product_id.uom_id.rounding)
            if (not supplierinfo.product_id and
                supplierinfo.product_tmpl_id and
                    supplierinfo.product_tmpl_id.uom_id):
                product_tmpl = supplierinfo.product_tmpl_id
                pending_to_receive = float_round(
                    move_data.get(product_tmpl.id, 0),
                    precision_rounding=product_tmpl.uom_id.rounding)
            supplierinfo.supplier_pending_to_receive = pending_to_receive
