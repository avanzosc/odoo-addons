# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models
from odoo.addons.base_import_wizard.models.base_import import convert2str
import xlrd


class ProductImport(models.Model):
    _inherit = "product.import"

    supplierinfo_import_id = fields.Many2one(
        string="Supplierinfo Import",
        comodel_name="product.supplierinfo.import",
        readonly=True)

    def _get_line_values(self, row_values={}):
        self.ensure_one()
        values = super()._get_line_values(row_values=row_values)
        if row_values:
            supplier_code = row_values.get("Supplier Code", "")
            supplier_name = row_values.get("Supplier Name", "")
            supplier_product_code = row_values.get("Supplier Product Code", "")
            supplier_product_name = row_values.get("Supplier Product Name", "")
            quantity = row_values.get("Quantity", "")
            price = row_values.get("Price", "")
            discount = row_values.get("Discount", "")
            delay = row_values.get("Delay", "")
            currency = row_values.get("Currency", "")
            date_start = row_values.get("Date Start", "")
            date_end = row_values.get("Date End", "")
            if date_start:
                date_start = xlrd.xldate.xldate_as_datetime(date_start, 0)
                date_start = date_start.date()
            elif not date_start:
                date_start = False
            if date_end:
                date_end = xlrd.xldate.xldate_as_datetime(date_end, 0)
                date_end = date_end.date()
            elif not date_end:
                date_end = False
            values.update({
                "supplier_code": convert2str(supplier_code),
                "supplier_name": supplier_name.title(),
                "supplier_product_code": convert2str(supplier_product_code),
                "supplier_product_name": convert2str(supplier_product_name),
                "quantity": quantity,
                "price": price,
                "discount": discount,
                "delay": delay,
                "currency": currency,
                "date_start": date_start,
                "date_end": date_end,
                }
            )
        return values

    def action_import_supplierinfo(self):
        self.ensure_one()
        supplierinfo_import = self.supplierinfo_import_id
        if not self.supplierinfo_import_id:
            supplierinfo_import = (
                self.env["product.supplierinfo.import"].create({
                    "file_date": fields.Date.today(),
                    "company_id": self.company_id.id,
                    "filename": self.filename}))
            self.supplierinfo_import_id = supplierinfo_import.id
        for line in self.import_line_ids.filtered(
            lambda l: l.state == "done" and not (
                l.import_supplierinfo_line_id)):
            supplierinfo_import_line = (
                self.env["product.supplierinfo.import.line"].create({
                    "product_name": line.product_name,
                    "product_code": line.product_default_code,
                    "product_id": line.product_id.id,
                    "supplier_code": line.supplier_code,
                    "supplier_name": line.supplier_name,
                    "supplier_product_code": line.supplier_product_code,
                    "supplier_product_name": line.supplier_product_name,
                    "quantity": line.quantity,
                    "price": line.price,
                    "discount": line.discount,
                    "delay": line.delay,
                    "currency": line.currency,
                    "date_start": line.date_start,
                    "date_end": line.date_end,
                    "import_id": supplierinfo_import.id}))
            line.import_supplierinfo_line_id = supplierinfo_import_line.id

    def action_view_supplierinfo_import(self):
        context = self.env.context.copy()
        return {
            "name": _("Supplierinfo Import"),
            "view_mode": "tree,form",
            "res_model": "product.supplierinfo.import",
            "domain": [("id", "=", self.supplierinfo_import_id.ids)],
            "type": "ir.actions.act_window",
            "context": context
        }
