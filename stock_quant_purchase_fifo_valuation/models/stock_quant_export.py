import base64
import io
from datetime import datetime

import xlsxwriter

from odoo import _, models
from odoo.exceptions import UserError


class StockQuant(models.Model):
    _inherit = "stock.quant"

    def action_export_purchase_fifo_xlsx(self):
        quants = self
        if not quants:
            raise UserError(_("No quants selected."))

        quants = quants.filtered(
            lambda q: q.product_id and q.product_id.tracking == "none"
        )
        if not quants:
            raise UserError(
                _("The selected quants do not contain NON‑traceable products.")
            )
        company = self.env.company
        onhand_by_product = {}
        products, onhand_by_product = self._get_products(quants, onhand_by_product)
        pol = self.env["purchase.order.line"].search(
            [
                ("product_id", "in", products.ids),
                ("order_id.state", "in", ["purchase", "done"]),
                ("order_id.company_id", "=", company.id),
            ]
        )
        pol = pol.sorted(
            key=lambda line: (line.order_id.date_order, line.id),
            reverse=True,
        )
        from collections import defaultdict

        lines_by_product = defaultdict(list)
        for line in pol:
            available = max(float(line.qty_received or 0.0), 0.0)
            lines_by_product[line.product_id.id].append(
                {"line": line, "available": available}
            )
        report_rows = []
        for product in products:
            total_stock = float(onhand_by_product.get(product.id, 0.0))
            if total_stock <= 0:
                continue
            remaining = total_stock
            rows_for_product = []
            plines = lines_by_product.get(product.id, [])
            rows_for_product, remaining = self._update_rows_for_product(
                plines, rows_for_product, product, company, remaining
            )
            uom = product.uom_id.name or ""
            default_code = product.default_code or ""
            pname = product.display_name or product.name
            for r in rows_for_product:
                subtotal = float(r["assigned_qty"]) * float(r["price_unit"])
                total_shipping_cost = float(r["assigned_qty"]) * float(
                    r["shipping_unit_cost"]
                )
                total_cost = subtotal + total_shipping_cost
                average_price = total_cost / float(r["assigned_qty"])
                report_rows.append(
                    {
                        "product_name": pname,
                        "default_code": default_code,
                        "uom": uom,
                        "onhand": total_stock,
                        "po_name": r["po_name"],
                        "vendor": r["vendor"],
                        "date_order": r["date_order"],
                        "shipping_unit_cost": r["shipping_unit_cost"],
                        "currency": r["currency"],
                        "price_unit": r["price_unit"],
                        "qty": r["assigned_qty"],
                        "subtotal": subtotal,
                        "total_shipping_cost": total_shipping_cost,
                        "total_cost": total_cost,
                        "average_price": average_price,
                    }
                )
        if not report_rows:
            raise UserError(_("No rows to export with the current selection."))
        output = io.BytesIO()
        wb = xlsxwriter.Workbook(output, {"in_memory": True})
        ws = wb.add_worksheet("Purchases_vs_Stock")
        fmt_hdr = wb.add_format(
            {"bold": True, "border": 1, "align": "center", "valign": "vcenter"}
        )
        fmt_txt = wb.add_format({"border": 1})
        fmt_eight = wb.add_format({"border": 1, "num_format": "#,##0.00000000"})
        fmt_four = wb.add_format({"border": 1, "num_format": "#,##0.0000"})
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
            _("Shipping Unit Cost"),
            _("Total Shipping Cost"),
            _("Total Cost"),
            _("Average Price"),
        ]
        for col, h in enumerate(headers):
            ws.write(0, col, h, fmt_hdr)

        ws.set_column(0, 0, 35)
        ws.set_column(1, 1, 10)
        ws.set_column(2, 2, 7)
        ws.set_column(3, 3, 14)
        ws.set_column(4, 4, 10)
        ws.set_column(5, 5, 40)
        ws.set_column(6, 6, 18)
        ws.set_column(7, 7, 10)
        ws.set_column(8, 14, 16)

        report_rows.sort(
            key=lambda r: (r["product_name"] or "", r["date_order"] or datetime.min),
            reverse=True,
        )
        row = 1
        for rec in report_rows:
            ws.write(row, 0, rec["product_name"] or "", fmt_txt)
            ws.write(row, 1, rec["default_code"] or "", fmt_txt)
            ws.write(row, 2, rec["uom"] or "", fmt_txt)
            ws.write_number(row, 3, float(rec["onhand"] or 0.0), fmt_qty)
            ws.write(row, 4, rec["po_name"] or "", fmt_txt)
            ws.write(row, 5, rec["vendor"] or "", fmt_txt)
            if rec["date_order"]:
                ws.write_datetime(row, 6, rec["date_order"], fmt_date)
            else:
                ws.write(row, 6, "", fmt_txt)
            ws.write(row, 7, rec["currency"].name if rec["currency"] else "", fmt_txt)
            ws.write_number(row, 8, float(rec["price_unit"] or 0.0), fmt_eight)
            ws.write_number(row, 9, float(rec["qty"] or 0.0), fmt_qty)
            ws.write_number(row, 10, float(rec["subtotal"] or 0.0), fmt_qty)
            ws.write_number(row, 11, float(rec["shipping_unit_cost"] or 0.0), fmt_four)
            ws.write_number(row, 12, float(rec["total_shipping_cost"] or 0.0), fmt_qty)
            ws.write_number(row, 13, float(rec["total_cost"] or 0.0), fmt_qty)
            ws.write_number(row, 14, float(rec["average_price"] or 0.0), fmt_eight)
            row += 1

        total_qty = sum(r["qty"] or 0.0 for r in report_rows)
        total_subtotal = sum(r["subtotal"] or 0.0 for r in report_rows)
        total_shipping = sum(r["total_shipping_cost"] or 0.0 for r in report_rows)
        total_cost = total_subtotal + total_shipping
        average_price = total_cost / total_qty if total_qty else 0.0

        if row > 1:
            ws.write(row, 8, "TOTAL", fmt_hdr)
            ws.write_number(row, 9, total_qty, fmt_qty)
            ws.write_number(row, 10, total_subtotal, fmt_qty)
            ws.write_number(row, 12, total_shipping, fmt_qty)
            ws.write_number(row, 13, total_cost, fmt_qty)
            ws.write_number(row, 14, average_price, fmt_eight)

        wb.close()
        output.seek(0)

        filename = (
            f'{_("purchases_vs_stock_non_traceable")}_'
            f'{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        )
        attachment = self.env["ir.attachment"].create(
            {
                "name": filename,
                "type": "binary",
                "datas": base64.b64encode(output.read()),
                "mimetype": (
                    "application/"
                    "vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                ),
                "res_model": "stock.quant",
                "res_id": self.ids and self.ids[0] or False,
            }
        )

        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attachment.id}?download=true",
            "target": "self",
        }

    def _get_products(self, quants, onhand_by_product):
        products = self.env["product.product"]
        for q in quants:
            pid = q.product_id.id
            onhand_by_product[pid] = onhand_by_product.get(pid, 0.0) + float(
                q.quantity or 0.0
            )
            products |= q.product_id
        if not products:
            raise UserError(_("No products in the selection."))
        return products, onhand_by_product

    def _update_rows_for_product(
        self, plines, rows_for_product, product, company, remaining
    ):
        if not plines:
            rows_for_product.append(
                {
                    "po_name": "—",
                    "vendor": "—",
                    "date_order": None,
                    "currency": product.currency_id or company.currency_id,
                    "price_unit": 0.0,
                    "assigned_qty": remaining,
                    "shipping_unit_cost": 0.0,
                }
            )
            remaining = 0.0
        else:
            for item in plines:
                if remaining <= 0:
                    break
                line = item["line"]
                available = float(item["available"])
                take = min(available, remaining)
                if take > 0:
                    rows_for_product.append(
                        {
                            "po_name": line.order_id.name or "",
                            "vendor": line.order_id.partner_id.display_name or "",
                            "date_order": line.order_id.date_order,
                            "currency": line.order_id.currency_id
                            or company.currency_id,
                            "price_unit": float(line.price_unit or 0.0),
                            "assigned_qty": take,
                            "shipping_unit_cost": float(
                                line.order_id.shipping_cost or 0.0
                            ),
                        }
                    )
                    remaining -= take
            if remaining != 0:
                if rows_for_product:
                    target = rows_for_product[0]
                else:
                    first_line = plines[0]["line"]
                    target = {
                        "po_name": first_line.order_id.name or "",
                        "vendor": first_line.order_id.partner_id.display_name or "",
                        "date_order": first_line.order_id.date_order,
                        "currency": first_line.order_id.currency_id
                        or company.currency_id,
                        "price_unit": float(first_line.price_unit or 0.0),
                        "assigned_qty": 0.0,
                        "shipping_unit_cost": float(
                            first_line.order_id.shipping_cost or 0.0
                        ),
                    }
                    rows_for_product.append(target)
                target["assigned_qty"] = float(target.get("assigned_qty", 0.0)) + float(
                    remaining
                )
                remaining = 0.0
        return rows_for_product, remaining
