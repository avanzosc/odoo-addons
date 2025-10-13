# -*- coding: utf-8 -*-
from odoo import api, models, _
from odoo.exceptions import UserError
from datetime import datetime
import io
import base64
import xlsxwriter

class StockQuant(models.Model):
    _inherit = "stock.quant"

    def action_export_purchase_fifo_xlsx(self):
        quants = self
        if not quants:
            raise UserError(_("No quants selected."))

        quants = quants.filtered(lambda q: q.product_id and q.product_id.tracking == 'none')
        if not quants:
            raise UserError(_("The selected quants do not contain NON‑traceable products."))

        company = self.env.company
        onhand_by_product = {}
        products = self.env['product.product']
        for q in quants:
            pid = q.product_id.id
            onhand_by_product[pid] = onhand_by_product.get(pid, 0.0) + float(q.quantity or 0.0)
            products |= q.product_id

        if not products:
            raise UserError(_("No products in the selection."))

        pol = self.env['purchase.order.line'].search([
            ('product_id', 'in', products.ids),
            ('order_id.state', 'in', ['purchase', 'done']),
            ('order_id.company_id', '=', company.id),
        ])
        pol = pol.sorted(key=lambda l: (l.order_id.date_order, l.id))

        from collections import defaultdict
        lines_by_product = defaultdict(list)
        for line in pol:
            available = max(float(line.qty_received or 0.0), 0.0)
            lines_by_product[line.product_id.id].append({'line': line, 'available': available})

        report_rows = []
        for product in products:
            total_stock = float(onhand_by_product.get(product.id, 0.0))
            if total_stock <= 0:
                continue
            remaining = total_stock
            rows_for_product = []
            plines = lines_by_product.get(product.id, [])
            if not plines:
                rows_for_product.append({'po_name': '—','vendor': '—','date_order': None,
                    'currency': product.currency_id or company.currency_id,'price_unit': 0.0,'assigned_qty': remaining})
                remaining = 0.0
            else:
                for item in plines:
                    if remaining <= 0:
                        break
                    line = item['line']
                    available = float(item['available'])
                    take = min(available, remaining)
                    if take > 0:
                        rows_for_product.append({
                            'po_name': line.order_id.name or '',
                            'vendor': line.order_id.partner_id.display_name or '',
                            'date_order': line.order_id.date_order,
                            'currency': line.order_id.currency_id or company.currency_id,
                            'price_unit': float(line.price_unit or 0.0),
                            'assigned_qty': take,
                        })
                        remaining -= take
                if remaining != 0:
                    if rows_for_product:
                        target = rows_for_product[0]
                    else:
                        first_line = plines[0]['line']
                        target = {'po_name': first_line.order_id.name or '',
                                  'vendor': first_line.order_id.partner_id.display_name or '',
                                  'date_order': first_line.order_id.date_order,
                                  'currency': first_line.order_id.currency_id or company.currency_id,
                                  'price_unit': float(first_line.price_unit or 0.0),
                                  'assigned_qty': 0.0}
                        rows_for_product.append(target)
                    target['assigned_qty'] = float(target.get('assigned_qty', 0.0)) + float(remaining)
                    remaining = 0.0

            uom = product.uom_id.name or ''
            default_code = product.default_code or ''
            pname = product.display_name or product.name
            for r in rows_for_product:
                subtotal = float(r['assigned_qty']) * float(r['price_unit'])
                report_rows.append({
                    'product_name': pname,'default_code': default_code,'uom': uom,'onhand': total_stock,
                    'po_name': r['po_name'],'vendor': r['vendor'],'date_order': r['date_order'],
                    'currency': r['currency'],'price_unit': r['price_unit'],'qty': r['assigned_qty'],
                    'subtotal': subtotal,
                })

        if not report_rows:
            raise UserError(_("No rows to export with the current selection."))

        output = io.BytesIO()
        wb = xlsxwriter.Workbook(output, {"in_memory": True})
        ws = wb.add_worksheet("Purchases_vs_Stock")

        fmt_hdr = wb.add_format({"bold": True, "border": 1, "align": "center", "valign": "vcenter"})
        fmt_txt = wb.add_format({"border": 1})
        fmt_num = wb.add_format({"border": 1, "num_format": "#,##0.00"})
        fmt_qty = wb.add_format({"border": 1, "num_format": "#,##0.00"})
        fmt_date = wb.add_format({"border": 1, "num_format": "yyyy-mm-dd hh:mm"})

        headers = [
            _("Product"),
            _("Reference"),
            _("UoM"),
            _("Stock (on‑hand)"),
            _("Order"),
            _("Vendor"),
            _("Order Date"),
            _("Currency"),
            _("Unit Price"),
            _("Assigned Qty"),
            _("Subtotal"),
        ]
        for col, h in enumerate(headers):
            ws.write(0, col, h, fmt_hdr)

        ws.set_column(0, 0, 40); ws.set_column(1, 1, 18); ws.set_column(2, 2, 10)
        ws.set_column(3, 3, 14); ws.set_column(4, 4, 16); ws.set_column(5, 5, 26)
        ws.set_column(6, 6, 18); ws.set_column(7, 7, 10); ws.set_column(8,10,16)

        report_rows.sort(key=lambda r: (r['product_name'] or '', r['date_order'] or datetime.min))
        row = 1
        for rec in report_rows:
            ws.write(row,0,rec['product_name'] or '',fmt_txt)
            ws.write(row,1,rec['default_code'] or '',fmt_txt)
            ws.write(row,2,rec['uom'] or '',fmt_txt)
            ws.write_number(row,3,float(rec['onhand'] or 0.0),fmt_qty)
            ws.write(row,4,rec['po_name'] or '',fmt_txt)
            ws.write(row,5,rec['vendor'] or '',fmt_txt)
            if rec['date_order']: ws.write_datetime(row,6,rec['date_order'],fmt_date)
            else: ws.write(row,6,'',fmt_txt)
            ws.write(row,7,rec['currency'].name if rec['currency'] else '',fmt_txt)
            ws.write_number(row,8,float(rec['price_unit'] or 0.0),fmt_num)
            ws.write_number(row,9,float(rec['qty'] or 0.0),fmt_qty)
            ws.write_number(row,10,float(rec['subtotal'] or 0.0),fmt_num)
            row += 1

        if row > 1:
            ws.write(row,9,"TOTAL",fmt_hdr)
            ws.write_formula(row,10,"=SUM(K2:K%s)" % row,fmt_num)

        wb.close(); output.seek(0)

        filename = "%s_%s.xlsx" % (_("purchases_vs_stock_non_traceable"), datetime.now().strftime("%Y%m%d_%H%M%S"))
        attachment = self.env['ir.attachment'].create({
            "name": filename,
            "type": "binary",
            "datas": base64.b64encode(output.read()),
            "mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "res_model": "stock.quant",
            "res_id": self.ids and self.ids[0] or False,
        })

        return {
            "type": "ir.actions.act_url",
            "url": "/web/content/%s?download=true" % attachment.id,
            "target": "self",
        }
