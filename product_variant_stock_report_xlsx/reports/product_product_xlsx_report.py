# Copyright 2026 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, models


class CatalogProductXlsx(models.AbstractModel):
    _name = "report.stock.product_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Product XLSX Report"

    def _get_record_name(self, record, field_name):
        if field_name not in record._fields:
            return ""
        value = record[field_name]
        return value.display_name or "" if value else ""

    def _get_monetary_num_format(self, currency):
        if not currency or not currency.decimal_places:
            return "#,##0"
        return f"#,##0.{'0' * currency.decimal_places}"

    def _get_orderpoints_by_product(self, products, company):
        orderpoints = self.env["stock.warehouse.orderpoint"].search(
            [
                ("product_id", "in", products.ids),
                ("company_id", "=", company.id),
            ],
            order="product_id, location_id, id",
        )
        orderpoints_by_product = {}
        for orderpoint in orderpoints:
            orderpoints_by_product.setdefault(orderpoint.product_id.id, orderpoint)
        return orderpoints_by_product

    def generate_xlsx_report(self, workbook, data, objects):
        force_company_id = data.get("force_company_id")
        company = (
            self.env["res.company"].browse(force_company_id).exists()
            if force_company_id
            else self.env.company
        )
        if not company:
            company = self.env.company
        objects = objects.with_company(company)
        orderpoints_by_product = self._get_orderpoints_by_product(objects, company)

        header_bold_props = {
            "text_wrap": True,
            "bold": True,
            "align": "center",
            "valign": "vjustify",
            "border": 1,
        }
        title = workbook.add_format(header_bold_props)
        table_header = workbook.add_format(
            dict(**header_bold_props, fg_color="#D7E4BC")
        )
        detail_props = {
            "border": 1,
            "valign": "vcenter",
        }
        table_detail_left = workbook.add_format(
            dict(
                **detail_props,
                align="left",
                num_format=self._get_monetary_num_format(company.currency_id),
            )
        )
        table_detail_right_price = workbook.add_format(
            dict(
                **detail_props,
                align="right",
                num_format=self._get_monetary_num_format(company.currency_id),
            )
        )
        table_detail_right_float = workbook.add_format(
            dict(**detail_props, align="right")
        )
        table_detail_right_float.set_num_format(4)  # Same as #,##0.00
        table_detail_right_int = workbook.add_format(
            dict(**detail_props, align="right")
        )
        table_detail_right_int.set_num_format(1)  # Same as 0

        worksheet = workbook.add_worksheet(_("PRODUCT LIST"))
        worksheet.set_landscape()
        worksheet.fit_to_pages(1, 0)
        worksheet.set_zoom(80)

        worksheet.merge_range(0, 0, 0, 29, _("MASTER DATA"), title)
        worksheet.write(1, 0, _("ID"), table_header)
        worksheet.set_column(0, 0, 10)
        worksheet.write(1, 1, _("Internal Reference"), table_header)
        worksheet.write(1, 2, _("Barcode"), table_header)
        worksheet.set_column(1, 2, 20)
        worksheet.write(1, 3, _("Name"), table_header)
        worksheet.write(1, 4, _("Description"), table_header)
        worksheet.set_column(3, 4, 60)
        worksheet.write(1, 5, _("Product Type"), table_header)
        worksheet.write(1, 6, _("Sales"), table_header)
        worksheet.write(1, 7, _("Purchase"), table_header)
        worksheet.set_column(5, 7, 15)
        worksheet.write(1, 8, _("Product Category"), table_header)
        worksheet.write(1, 9, _("Brand"), table_header)
        worksheet.write(1, 10, _("Family"), table_header)
        worksheet.write(1, 11, _("Subfamily"), table_header)
        worksheet.write(1, 12, _("Season"), table_header)
        worksheet.write(1, 13, _("Serie"), table_header)
        worksheet.set_column(8, 13, 40)
        worksheet.write(1, 14, _("Expense Account"), table_header)
        worksheet.write(1, 15, _("Income Account"), table_header)
        worksheet.set_column(14, 15, 30)
        worksheet.write(1, 16, _("Sales Price"), table_header)
        worksheet.write(1, 17, _("Cost"), table_header)
        worksheet.write(1, 18, _("Unit of Measure"), table_header)
        worksheet.write(1, 19, _("Purchase Unit"), table_header)
        worksheet.write(1, 20, _("Vendor"), table_header)
        worksheet.write(1, 21, _("Routes"), table_header)
        worksheet.write(1, 22, _("Track Inventory"), table_header)
        worksheet.write(1, 23, _("Sales Taxes"), table_header)
        worksheet.write(1, 24, _("Min Quantity"), table_header)
        worksheet.write(1, 25, _("Max Quantity"), table_header)
        worksheet.write(1, 26, _("Quantity Multiple"), table_header)
        worksheet.write(1, 27, _("Customer Lead Time"), table_header)
        worksheet.write(1, 28, _("Weight"), table_header)
        worksheet.write(1, 29, _("Volume"), table_header)

        attr_column = start_attr_column = 30
        all_attributes = (
            objects.mapped("product_tmpl_id.attribute_line_ids.attribute_id")
            | objects.mapped("product_template_attribute_value_ids.attribute_id")
        ).sorted()
        for attribute in all_attributes:
            worksheet.write(1, attr_column, attribute.display_name, table_header)
            attr_column += 1
        if all_attributes:
            worksheet.merge_range(
                0,
                start_attr_column,
                0,
                attr_column - 1,
                _("ATTRIBUTES"),
                title,
            )
            worksheet.set_column(start_attr_column, attr_column - 1, 30)

        row_num = 2
        for product in objects:
            worksheet.write(row_num, 0, product.id, table_detail_right_int)
            worksheet.write(row_num, 1, product.default_code or "", table_detail_left)
            worksheet.write(row_num, 2, product.barcode or "", table_detail_left)
            worksheet.write(row_num, 3, product.name, table_detail_left)
            worksheet.write(row_num, 4, product.name, table_detail_left)
            worksheet.write(row_num, 5, product.type, table_detail_left)
            worksheet.write(row_num, 6, product.sale_ok, table_detail_left)
            worksheet.write(row_num, 7, product.purchase_ok, table_detail_left)
            worksheet.write(row_num, 8, product.categ_id.name, table_detail_left)
            worksheet.write(
                row_num,
                9,
                self._get_record_name(product, "product_brand_id"),
                table_detail_left,
            )
            worksheet.write(
                row_num,
                10,
                self._get_record_name(product, "family_id"),
                table_detail_left,
            )
            worksheet.write(
                row_num,
                11,
                self._get_record_name(product, "sub_family_id"),
                table_detail_left,
            )
            worksheet.write(
                row_num,
                12,
                self._get_record_name(product, "season_id"),
                table_detail_left,
            )
            worksheet.write(
                row_num,
                13,
                self._get_record_name(product, "serie_id"),
                table_detail_left,
            )

            accounts = product._get_product_accounts()
            account_income = accounts.get("income")
            account_expense = accounts.get("expense")
            worksheet.write(
                row_num,
                14,
                account_expense and account_expense.code or "",
                table_detail_left,
            )
            worksheet.write(
                row_num,
                15,
                account_income and account_income.code or "",
                table_detail_left,
            )

            worksheet.write(row_num, 16, product.lst_price, table_detail_right_price)
            worksheet.write(
                row_num, 17, product.standard_price, table_detail_right_price
            )
            worksheet.write(row_num, 18, product.uom_id.name, table_detail_left)
            worksheet.write(row_num, 19, product.uom_po_id.name, table_detail_left)

            supplierinfo_list = []
            for vendor in product._prepare_sellers():
                supplierinfo_list.append(
                    f"{vendor.partner_id.name} "
                    f"{vendor.min_qty:g}*{vendor.price:g}*"
                    f"{vendor.currency_id.name or ''}"
                )
            worksheet.write(row_num, 20, "|".join(supplierinfo_list), table_detail_left)

            routes = "|".join(product.route_ids.mapped("name"))
            worksheet.write(row_num, 21, routes, table_detail_left)
            worksheet.write(row_num, 22, product.tracking, table_detail_left)
            taxes = product.taxes_id.filtered(
                lambda tax: not tax.company_id or tax.company_id == company
            )
            worksheet.write(
                row_num, 23, ",".join(taxes.mapped("name")), table_detail_left
            )

            orderpoint = orderpoints_by_product.get(product.id)
            worksheet.write(
                row_num,
                24,
                orderpoint.product_min_qty if orderpoint else "",
                table_detail_right_float,
            )
            worksheet.write(
                row_num,
                25,
                orderpoint.product_max_qty if orderpoint else "",
                table_detail_right_float,
            )
            worksheet.write(
                row_num,
                26,
                orderpoint.qty_multiple if orderpoint else "",
                table_detail_right_float,
            )
            worksheet.write(
                row_num,
                27,
                orderpoint.days_to_order if orderpoint else "",
                table_detail_right_int,
            )

            worksheet.write(row_num, 28, product.weight, table_detail_right_float)
            worksheet.write(row_num, 29, product.volume, table_detail_right_float)

            attr_value_col = start_attr_column
            for attribute in all_attributes:
                attribute_value = product.product_template_attribute_value_ids.filtered(
                    lambda value, attr=attribute: value.attribute_id == attr
                )
                worksheet.write(
                    row_num,
                    attr_value_col,
                    attribute_value.name or "",
                    table_detail_left,
                )
                attr_value_col += 1
            row_num += 1
