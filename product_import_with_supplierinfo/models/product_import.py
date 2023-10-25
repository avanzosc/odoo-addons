# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from xlrd.xldate import xldate_as_datetime

from odoo import _, api, fields, models

from odoo.addons.base_import_wizard.models.base_import import convert2str


class ProductImport(models.Model):
    _inherit = "product.import"

    supplierinfo_import_id = fields.Many2one(
        string="Supplierinfo Import",
        comodel_name="product.supplierinfo.import",
        readonly=True,
    )
    show_supplierinfo_import = fields.Boolean(
        compute="_compute_show_supplierinfo_import",
        store=True,
    )

    @api.depends(
        "supplierinfo_import_id",
        "import_line_ids",
        "import_line_ids.supplier_code",
        "import_line_ids.supplier_name",
        "import_line_ids.product_id",
        "import_line_ids.product_name",
        "import_line_ids.product_default_code",
    )
    def _compute_show_supplierinfo_import(self):
        for record in self:
            record.show_supplierinfo_import = bool(
                record.supplierinfo_import_id
            ) or any(
                record.mapped("import_line_ids.supplier_name")
                + record.mapped("import_line_ids.supplier_code")
            )

    def _get_line_values(self, row_values=False):
        self.ensure_one()
        values = super()._get_line_values(row_values=row_values)
        if row_values:
            supplier_code = row_values.get("Supplier Code", "")
            supplier_name = row_values.get("Supplier Name", "")
            if not supplier_code and not supplier_name:
                return values
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
                date_start = xldate_as_datetime(date_start, 0)
                date_start = date_start.date()
            if date_end:
                date_end = xldate_as_datetime(date_end, 0)
                date_end = date_end.date()
            values.update(
                {
                    "supplier_code": convert2str(supplier_code),
                    "supplier_name": supplier_name.title(),
                    "supplier_product_code": convert2str(supplier_product_code),
                    "supplier_product_name": convert2str(supplier_product_name),
                    "quantity": quantity,
                    "price": price,
                    "discount": discount,
                    "delay": delay,
                    "currency": currency,
                    "date_start": date_start or False,
                    "date_end": date_end or False,
                }
            )
        return values

    def action_import_supplierinfo(self):
        self.ensure_one()
        if not self.show_supplierinfo_import:
            return {}
        if self.show_supplierinfo_import and not self.supplierinfo_import_id:
            self.supplierinfo_import_id = self.env[
                "product.supplierinfo.import"
            ].create(
                {
                    "file_date": fields.Date.today(),
                    "company_id": self.company_id.id,
                    "filename": self.filename,
                    "import_type": "supplierinfo",
                },
            )
        supplierinfo_import_lines = self.import_line_ids.filtered(
            lambda ln: ln.state == "done"
            and (ln.supplier_name or ln.supplier_code)
            and ln.product_id
            and not ln.import_supplierinfo_line_id
        )
        if self.supplierinfo_import_id and supplierinfo_import_lines:
            for line in supplierinfo_import_lines:
                line._create_supplierinfo_import_line()
        context = self.env.context.copy()
        return {
            "name": _("Supplierinfo Import"),
            "view_mode": "form",
            "res_model": "product.supplierinfo.import",
            "res_id": self.supplierinfo_import_id.id,
            "type": "ir.actions.act_window",
            "context": context,
        }
