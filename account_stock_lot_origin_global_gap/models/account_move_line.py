# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models
from collections import defaultdict
from odoo.tools import float_is_zero, float_compare
from odoo.tools.misc import formatLang


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _get_invoiced_lot_values(self):
        manufacture = self.env.ref("mrp.route_warehouse0_manufacture")
        self.ensure_one()
        res = []
        if (self.move_id.state == 'draft' or not
            self.move_id.invoice_date or
                self.move_id.move_type not in ('out_invoice', 'out_refund')):
            return res
        current_invoice_amls = self.filtered(
            lambda aml: aml.display_type == 'product' and
            aml.product_id and aml.product_id.type in ('consu', 'product') and
            aml.quantity)
        invoice_lines = current_invoice_amls.sale_line_ids.invoice_lines
        all_invoices_amls = invoice_lines.filtered(
            lambda aml: aml.move_id.state == 'posted').sorted(
                lambda aml: (aml.date, aml.move_name, aml.id))
        index = (all_invoices_amls.ids.index(current_invoice_amls[:1].id) if
                 current_invoice_amls[:1] in all_invoices_amls else 0)
        previous_amls = all_invoices_amls[:index]
        invoiced_qties = current_invoice_amls._get_invoiced_qty_per_product()
        invoiced_products = invoiced_qties.keys()
        if self.move_id.move_type == 'out_invoice':
            previous_amls = previous_amls.filtered(
                lambda aml: aml.move_id.payment_state != 'reversed')
        previous_qties_invoiced = previous_amls._get_invoiced_qty_per_product()
        if self.move_id.move_type == 'out_refund':
            for p in previous_qties_invoiced:
                previous_qties_invoiced[p] = -previous_qties_invoiced[p]
            for p in invoiced_qties:
                invoiced_qties[p] = -invoiced_qties[p]
        qties_per_lot = defaultdict(float)
        previous_qties_delivered = defaultdict(float)
        move_line_ids = (
            current_invoice_amls.sale_line_ids.move_ids.move_line_ids)
        stock_move_lines = move_line_ids.filtered(
            lambda sml: sml.state == 'done' and sml.lot_id).sorted(
                lambda sml: (sml.date, sml.id))
        for sml in stock_move_lines:
            if (sml.product_id not in invoiced_products or 'customer' not in
                    {sml.location_id.usage, sml.location_dest_id.usage}):
                continue
            product = sml.product_id
            product_uom = product.uom_id
            qty_done = sml.product_uom_id._compute_quantity(
                sml.qty_done, product_uom)
            is_stock_return = (
                self.move_id.move_type == 'out_invoice' and (
                    sml.location_id.usage,
                    sml.location_dest_id.usage) == ('customer', 'internal') or
                self.move_id.move_type == 'out_refund' and
                (sml.location_id.usage,
                 sml.location_dest_id.usage) == ('internal', 'customer'))
            if is_stock_return:
                returned_qty = min(qties_per_lot[sml.lot_id], qty_done)
                qties_per_lot[sml.lot_id] -= returned_qty
                qty_done = returned_qty - qty_done
            previous_qty_invoiced = previous_qties_invoiced[product]
            previous_qty_delivered = previous_qties_delivered[product]
            if float_compare(
                qty_done, 0, precision_rounding=product_uom.rounding) < 0 or \
                    float_compare(
                        previous_qty_delivered, previous_qty_invoiced,
                        precision_rounding=product_uom.rounding) < 0:
                previously_done = (
                    qty_done if is_stock_return else
                    min(previous_qty_invoiced - previous_qty_delivered,
                        qty_done))
                previous_qties_delivered[product] += previously_done
                qty_done -= previously_done
            qties_per_lot[sml.lot_id] += qty_done
        for lot, qty in qties_per_lot.items():
            # access the lot as a superuser in order to avoid an error
            # when a user prints an invoice without having the stock access
            lot = lot.sudo()
            if (float_is_zero(
                invoiced_qties[lot.product_id],
                precision_rounding=lot.product_uom_id.rounding) or
                float_compare(
                    qty, 0,
                    precision_rounding=lot.product_uom_id.rounding) <= 0):
                continue
            invoiced_lot_qty = min(qty, invoiced_qties[lot.product_id])
            invoiced_qties[lot.product_id] -= invoiced_lot_qty
            res.append({
                'product_name': lot.product_id.display_name,
                'quantity': formatLang(
                    self.env, invoiced_lot_qty, dp='Product Unit of Measure'),
                'uom_name': lot.product_uom_id.name,
                'lot_name': lot.name,
                'lot_id': lot.id,
            })
        if not res:
            return res
        if self.move_id.move_type != "out_invoice":
            for line in res:
                line = self.put_origin_global_gap_case1(line)
        else:
            for line in res:
                invoice_line = self.filtered(
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
        print ('***** res: ' + str(res))
        return res

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
