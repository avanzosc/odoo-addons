# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import base64
import io
import os
from datetime import timedelta

import xlsxwriter

from odoo import api, fields, models
from odoo.tools import config

STOCK_FILE_RETENTION_DAYS = 15


class ResPartner(models.Model):
    _inherit = "res.partner"

    send_stock = fields.Boolean(
        string="Send Stock by Email",
        help="Every day this contact receives by email an Excel file with "
        "the available stock.",
    )

    @api.model
    def _get_stock_mail_products(self):
        return self.env["product.product"].search(
            [
                ("sale_ok", "=", True),
                ("purchase_ok", "=", True),
                ("is_published", "=", True),
            ]
        )

    @api.model
    def _get_stock_mail_file(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        header_format = workbook.add_format(
            {"bold": True, "border": 1, "align": "center", "valign": "vcenter"}
        )
        text_format = workbook.add_format({"border": 1})
        center_format = workbook.add_format(
            {"border": 1, "align": "center", "valign": "vcenter"}
        )
        price_format = workbook.add_format({"border": 1, "num_format": "#,##0.00"})
        sheet = workbook.add_worksheet("Stock Disponible")
        headers = [
            self.env._("Reference"),
            self.env._("Product"),
            self.env._("Sale Price"),
            self.env._("Barcode"),
            self.env._("Brand"),
            self.env._("Stock"),
        ]
        for col, header in enumerate(headers):
            sheet.write_string(0, col, header, header_format)
            sheet.set_column(col, col, 35 if col == 0 else 30)
        products = self.with_context(lang="en_US")._get_stock_mail_products()
        for row, product in enumerate(products, start=1):
            sheet.write_string(row, 0, product.default_code or "", center_format)
            sheet.write_string(row, 1, product.name or "", text_format)
            sheet.write_number(row, 2, product.lst_price, price_format)
            sheet.write_string(row, 3, product.barcode or "", center_format)
            sheet.write_string(row, 4, product.product_brand_id.name or "", text_format)
            sheet.write_number(row, 5, max(product.free_qty, 0.0), text_format)
        sheet.freeze_panes(1, 0)
        sheet.autofilter(0, 0, len(products), len(headers) - 1)
        workbook.close()
        return base64.b64encode(output.getvalue())

    @api.model
    def _get_stock_mail_file_name(self, date=None, lang=None):
        date = date or fields.Date.context_today(self)
        lang_suffix = f"_{lang}" if lang else ""
        return "stock_{}{}.xlsx".format(date.strftime("%Y_%m_%d"), lang_suffix)

    @api.model
    def _get_stock_mail_folder(self):
        return os.path.join(config["data_dir"], "export_stock", self.env.cr.dbname)

    @api.model
    def _save_stock_mail_file(self, file_name, datas):
        folder = self._get_stock_mail_folder()
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, file_name), "wb") as stock_file:
            stock_file.write(base64.b64decode(datas))
        limit_date = fields.Date.context_today(self) - timedelta(
            days=STOCK_FILE_RETENTION_DAYS
        )
        limit_date_name = limit_date.strftime("%Y_%m_%d")
        for old_name in os.listdir(folder):
            if (
                old_name.startswith("stock_")
                and old_name.endswith(".xlsx")
                and old_name[6:16] <= limit_date_name
            ):
                os.remove(os.path.join(folder, old_name))

    @api.model
    def _cron_send_stock_mail(self):
        langs = [code for code, _name in self.env["res.lang"].get_installed()]
        default_lang = "en_US" if "en_US" in langs else langs[0]
        partners = self.search([("send_stock", "=", True), ("email", "!=", False)])
        template = self.env.ref("stock_partner_daily_mail.mail_template_partner_stock")
        file_name = self._get_stock_mail_file_name()
        for lang in langs:
            datas = self.with_context(lang=lang)._get_stock_mail_file()
            self._save_stock_mail_file(self._get_stock_mail_file_name(lang=lang), datas)
            lang_partners = partners.filtered(
                lambda p, lang=lang: (p.lang if p.lang in langs else default_lang)
                == lang
            )
            if lang_partners:
                template.send_mail_batch(
                    lang_partners.ids,
                    force_send=True,
                    email_values={"attachments": [(file_name, datas)]},
                )
