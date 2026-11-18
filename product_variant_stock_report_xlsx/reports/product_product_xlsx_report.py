# Copyright 2026 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

from odoo import _, models

_logger = logging.getLogger(__name__)


class CatalogProductXlsx(models.AbstractModel):
    _name = "report.stock.product_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Product XLSX Report"

    def generate_xlsx_report(self, workbook, data, objects):
        force_company_id = data.get("force_company_id")

        ## XLSX Style definition
        header_bold_props = {
            "text_wrap": True,
            "bold": True,
            "align": "center",
            "valign": "vjustify",
            "border": 1,
        }
        # self.header_bold_style = self.workbook.add_format(header_bold_props)
        # self.header_bold_style_float = self.workbook.add_format(
        # dict(**header_bold_props, num_format='#,##0.00'))
        # self.header_bold_style_monetary = self.workbook.add_format(
        # dict(**header_bold_props, num_format=f'#,##0.{(decimal_places or 2) * "0"}'))

        title = workbook.add_format(header_bold_props)
        table_header = workbook.add_format(
            dict(**header_bold_props, fg_color="#D7E4BC")
        )

        detail_props = {
            "border": 1,
            "align": "left",
            "valign": "vcenter",
        }

        table_detail_left = workbook.add_format(detail_props)
        table_detail_right_num = workbook.add_format(
            {
                "border": 1,
                "align": "right",
                "valign": "vcenter",
            }
        )
        table_detail_right_num.set_num_format("#,##0.00")

        worksheet = workbook.add_worksheet(_("PRODUCT LIST"))
        worksheet.set_landscape()
        worksheet.fit_to_pages(1, 0)
        worksheet.set_zoom(80)

        worksheet.merge_range(0, 0, 0, 29, _("MASTER DATA"), title)
        worksheet.write(1, 0, "ID", table_header)
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

        all_attributes = objects.mapped(
            "product_variant_id.attribute_line_ids.attribute_id"
        ).sorted()

        for attribute in all_attributes:
            worksheet.write(1, attr_column, attribute.display_name, table_header)
            attr_column += 1
        worksheet.merge_range(
            0, start_attr_column, 0, attr_column - 1, _("ATTRIBUTES"), title
        )

        worksheet.set_column(start_attr_column, attr_column - 1, 40)  # Column Width

        row_num = 2
        for product in objects:
            worksheet.write(row_num, 0, product.id, table_detail_left)
            worksheet.write(row_num, 1, product.default_code, table_detail_left)
            worksheet.write(row_num, 2, product.barcode, table_detail_left)
            worksheet.write(row_num, 3, product.name, table_detail_left)
            worksheet.write(row_num, 4, product.name, table_detail_left)
            worksheet.write(row_num, 5, product.type, table_detail_left)
            worksheet.write(row_num, 6, product.purchase_ok, table_detail_left)
            worksheet.write(row_num, 7, product.sale_ok, table_detail_left)
            worksheet.write(row_num, 8, product.categ_id.name, table_detail_left)
            worksheet.write(
                row_num,
                9,
                product.product_brand_id and product.product_brand_id.name or "",
                table_detail_left,
            )
            worksheet.write(
                row_num,
                10,
                product.family_id and product.family_id.name or "",
                table_detail_left,
            )
            worksheet.write(
                row_num,
                11,
                product.sub_family_id and product.sub_family_id.name or "",
                table_detail_left,
            )
            worksheet.write(
                row_num,
                12,
                product.season_id and product.season_id.name or "",
                table_detail_left,
            )
            # worksheet.write(
            #     row_num, 13, product.serie_id and product.serie_id.name or '',
            #     table_detail_left)

            accounts = product.with_company(force_company_id)._get_product_accounts()
            account_income = accounts.get("income")
            worksheet.write(
                row_num,
                14,
                account_income and account_income.code or "",
                table_detail_left,
            )
            account_expense = accounts.get("expense")
            worksheet.write(
                row_num,
                15,
                account_expense and account_expense.code or "",
                table_detail_left,
            )

            worksheet.write(row_num, 16, product.lst_price, table_detail_right_num)
            worksheet.write(row_num, 17, product.standard_price, table_detail_right_num)
            worksheet.write(row_num, 18, product.uom_id.name, table_detail_left)
            worksheet.write(row_num, 19, product.uom_po_id.name, table_detail_left)

            supplierinfos = product.with_company(force_company_id).seller_ids
            supplierinfo_list = []
            for vendor in supplierinfos:
                supplierinfo_list.append(
                    f"{vendor.partner_id.name} "
                    "{vendor.min_qty}*{vendor.price}*{vendor.currency_id.name}"
                )
            suppliers_detail = "|".join(supplierinfo_list) if supplierinfo_list else ""
            worksheet.write(row_num, 20, suppliers_detail, table_detail_left)

            routes = (
                "|".join([route.name for route in product.route_ids])
                if product.route_ids
                else ""
            )

            worksheet.write(row_num, 21, routes, table_detail_left)
            worksheet.write(row_num, 22, product.tracking, table_detail_left)
            taxes_names = [tax.name for tax in product.taxes_id]
            taxes = ",".join(taxes_names) if product.taxes_id else ""
            worksheet.write(row_num, 23, taxes, table_detail_left)

            orderpoint = self.env["stock.warehouse.orderpoint"].search(
                [("product_id", "=", product.id)], limit=1
            )
            if orderpoint:
                worksheet.write(
                    row_num, 24, orderpoint.product_min_qty, table_detail_left
                )
                worksheet.write(
                    row_num, 25, orderpoint.product_max_qty, table_detail_left
                )
                worksheet.write(row_num, 26, orderpoint.qty_multiple, table_detail_left)
                # worksheet.write(
                #     row_num, 27, orderpoint.lead_days, table_detail_left)

            worksheet.write(row_num, 28, product.weight, table_detail_left)
            worksheet.write(row_num, 29, product.volume, table_detail_left)

            attr_value_col = start_attr_column
            for attribute in all_attributes:
                attribute_value = product.product_template_attribute_value_ids.filtered(
                    lambda a, attr=attribute: a.attribute_id == attr
                )
                worksheet.write(
                    row_num,
                    attr_value_col,
                    attribute_value.name or "",
                    table_detail_left,
                )
                attr_value_col += 1
            row_num += 1
