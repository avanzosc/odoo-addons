# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    with_origin_global_gap = fields.Boolean(
        string="With Origin/Global Gap",
        compute="_compute_with_origin_global_gap")

    def _compute_with_origin_global_gap(self):
        for invoice in self:
            with_origin_global_gap = False
            if invoice.move_type == "out_invoice":
                lines = invoice._get_invoiced_lot_values()
                if lines:
                    for line in lines:
                        if "lot_id" in line and line.get("lot_id", False):
                            lot = self.env["stock.lot"].browse(
                                line.get("lot_id"))
                            product = lot.product_id
                            if product.show_origin_global_gap_in_documents:
                                with_origin_global_gap = True
            invoice.with_origin_global_gap = with_origin_global_gap

    def _get_invoiced_lot_values(self):
        lines = super(AccountMove, self)._get_invoiced_lot_values()
        manufacture = self.env.ref("mrp.route_warehouse0_manufacture")
        if not lines:
            return lines
        if self.move_type != "out_invoice":
            for line in lines:
                line = self.put_origin_global_gap_case1(line)
        else:
            for line in lines:
                invoice_line = self.invoice_line_ids.filtered(
                    lambda x: x.name == line.get("product_name"))
                if not invoice_line:
                    line = self.put_origin_global_gap_case1(line)
                if (invoice_line and manufacture not in
                        invoice_line.product_id.route_ids):
                    line = self.put_origin_global_gap_case1(line)
                if (invoice_line and manufacture in
                        invoice_line.product_id.route_ids):
                    lot_country_to_print = ""
                    lot_global_gap_to_print = ""
                    for move in invoice_line.move_line_ids.filtered(
                            lambda x: x.created_production_id):
                        move_lines = move.created_production_id.move_raw_ids
                        move_lines = move_lines.filtered(
                            lambda x: x.state != "cancel" and
                            x.product_id.show_origin_global_gap_in_documents)
                        for ml in move_lines:
                            for move_line in ml.move_line_ids.filtered(
                                    lambda z: z.lot_id):
                                if move_line.lot_id.country_id:
                                    if not lot_country_to_print:
                                        lot_country_to_print = (
                                            move_line.lot_id.country_id.name)
                                    else:
                                        name = move_line.lot_id.country_id.name
                                        lot_country_to_print = (
                                            u"{}, {}".format(
                                                lot_country_to_print, name))
                                if move_line.lot_id.ref:
                                    if not lot_global_gap_to_print:
                                        lot_global_gap_to_print = (
                                            move_line.lot_id.ref)
                                    else:
                                        lot_global_gap_to_print = (
                                            u"{}, {}".format(
                                                lot_global_gap_to_print,
                                                move_line.lot_id.ref))
                    line["lot_origin"] = lot_country_to_print
                    line["lot_global_gap"] = lot_global_gap_to_print
        return lines

    def put_origin_global_gap_case1(self, line):
        line["lot_origin"] = ""
        line["lot_global_gap"] = ""
        if "lot_id" in line and line.get("lot_id", False):
            lot = self.env["stock.lot"].browse(
                line.get("lot_id"))
            if lot.product_id.show_origin_global_gap_in_documents:
                if lot.country_id:
                    line["lot_origin"] = lot.country_id.name
                if lot.ref:
                    line["lot_global_gap"] = lot.ref
        return line
