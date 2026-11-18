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
        title = workbook.add_format(
            {
                "bold": True,
                "align": "center",
                "valign": "vcenter",
            }
        )
        table_header = workbook.add_format(
            {
                "bold": True,
                "border": 1,
                "align": "center",
                "valign": "vcenter",
                "fg_color": "#D7E4BC",
            }
        )
        table_header.set_text_wrap()
        table_detail_left = workbook.add_format(
            {
                "border": 1,
                "align": "left",
                "valign": "vcenter",
            }
        )
        table_detail_right_num = workbook.add_format(
            {
                "border": 1,
                "align": "right",
                "valign": "vcenter",
            }
        )
        table_detail_right_num.set_num_format("#,##0.00")

        worksheet = workbook.add_worksheet("Hoja1")

        worksheet.merge_range(0, 0, 0, 29, "DATOS PRINCIPALES", title)
        worksheet.write(1, 0, "ID", table_header)
        worksheet.write(1, 1, _("Internal Reference"), table_header)
        worksheet.write(1, 2, _("Barcode"), table_header)
        worksheet.write(1, 3, _("Name"), table_header)
        worksheet.write(1, 4, "Descripción", table_header)
        worksheet.write(1, 5, _("Product Type"), table_header)
        worksheet.write(1, 6, _("Sales"), table_header)
        worksheet.write(1, 7, _("Purchase"), table_header)
        worksheet.write(1, 8, _("Product Category"), table_header)
        worksheet.write(1, 9, "Marca", table_header)
        worksheet.write(1, 10, "Familia", table_header)
        worksheet.write(1, 11, "Subfamilia", table_header)
        worksheet.write(1, 12, "Temporada", table_header)
        worksheet.write(1, 13, "SERIE", table_header)
        worksheet.write(1, 14, "Cuenta Contable Compra", table_header)
        worksheet.write(1, 15, "Cuenta Contable Venta", table_header)
        worksheet.write(1, 16, "Precio de venta", table_header)
        worksheet.write(1, 17, "Costo", table_header)
        worksheet.write(1, 18, "Unidad de medida", table_header)
        worksheet.write(1, 19, "Unidad de medida de compra", table_header)
        worksheet.write(1, 20, "Proveedor", table_header)
        worksheet.write(1, 21, "Abastecimiento", table_header)
        worksheet.write(1, 22, "Seguimiento", table_header)
        worksheet.write(1, 23, "Impuestos", table_header)
        worksheet.write(1, 24, "Stock minimo", table_header)
        worksheet.write(1, 25, "Stock máximo", table_header)
        worksheet.write(1, 26, "Múltiplo de cantidades", table_header)
        worksheet.write(1, 27, "Plazo de entrega (días)", table_header)
        worksheet.write(1, 28, "Peso", table_header)
        worksheet.write(1, 29, "Volumen", table_header)

        attr_column = start_attr_column = 30

        all_attributes = objects.mapped(
            "product_variant_id.attribute_line_ids.attribute_id"
        ).sorted()

        for attribute in all_attributes:
            worksheet.write(1, attr_column, attribute.display_name, table_header)
            attr_column += 1
        worksheet.merge_range(
            0, start_attr_column, 0, attr_column - 1, "ATRIBUTOS", title
        )

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
